import json
import logging
import operator
import os
import os.path
import re

import jsonschema
import six

from . import resolver, utils

logger = logging.getLogger("curate-bids")

DEFAULT_TEMPLATE_NAME = "default"
BIDS_V1_TEMPLATE_NAME = "bids-v1"
REPROIN_TEMPLATE_NAME = "reproin"

this_dir = os.path.dirname(os.path.realpath(__file__))
DEFAULT_TEMPLATE_DIR = os.path.join(this_dir, "../templates")


def load_and_normalize_json(path):
    with open(path, "r") as f:
        data = json.load(f)
    return utils.normalize_strings(data)


class Template:
    """Represents a project-level template for organizing data.

    Args:
        data (dict): The json configuration for the template

    Attributes:
        namespace (str): The namespace where resolved template data is displayed.
        description (str): The optional description of the template.
        definitions (dict): The map of template definitions.
        rules (list): The list of if rules for applying templates.
        extends (string): The optional name of the template to extend.
        exclude_rules (list): The optional list of rules to exclude from a parent template.
    """

    def __init__(self, data, save_sidecar_as_metadata=False):
        if data:
            self.namespace = data.get("namespace")
            self.description = data.get("description", "")
            self.definitions = data.get("definitions", {})
            self.rules = data.get("rules", [])
            self.upload_rules = data.get("upload_rules", [])
            self.resolvers = data.get("resolvers", [])
            self.custom_initializers = data.get("initializers", [])
            self.extends = data.get("extends")
            self.exclude_rules = data.get("exclude_rules", [])
        else:
            raise Exception("data is required")

        if self.extends:
            self.do_extend(save_sidecar_as_metadata)

        resolver = jsonschema.RefResolver.from_schema({"definitions": self.definitions})
        self.resolve_refs(resolver, self.definitions)
        self.compile_resolvers(save_sidecar_as_metadata)
        self.compile_rules()
        self.compile_custom_initializers()

    def do_extend(self, save_sidecar_as_metadata):
        """The template (json file) just read is an extension template so load the template
        that is to be extended (one of the defined templates).
        """
        logger.info("Extending project curation template: '%s'", self.extends)

        parent = load_template(
            template_name=self.extends,
            save_sidecar_as_metadata=save_sidecar_as_metadata,
        )

        if not self.namespace:
            self.namespace = parent.namespace

        my_rules = self.rules
        my_defs = self.definitions
        my_resolvers = self.resolvers
        my_initializers = self.custom_initializers

        # Extend definitions
        self.definitions = parent.definitions.copy()
        for key, value in my_defs.items():
            self.definitions[key] = value

        # Extend rules, after filtering excluded rules
        filtered_rules = filter(lambda x: x.id not in self.exclude_rules, parent.rules)
        self.rules = my_rules + list(filtered_rules)

        # Extend resolvers
        self.resolvers = my_resolvers + parent.resolvers

        self.custom_initializers = my_initializers + parent.custom_initializers

    def compile_rules(self):
        """Converts the rule dictionaries on this object to Rule class objects."""
        for i in range(0, len(self.rules)):
            rule = self.rules[i]
            if not isinstance(rule, Rule):
                self.rules[i] = Rule(rule)

        for i in range(0, len(self.upload_rules)):
            upload_rule = self.upload_rules[i]
            if not isinstance(upload_rule, Rule):
                self.upload_rules[i] = Rule(upload_rule)

    def compile_resolvers(self, save_sidecar_as_metadata=False):
        """Walk through the definitions."""
        self.resolver_map = {}
        for i in range(0, len(self.resolvers)):
            res = self.resolvers[i]
            if not isinstance(res, resolver.Resolver):
                res = resolver.Resolver(self.namespace, res, save_sidecar_as_metadata)

            # Create a mapping of template id to resolver
            for tmpl in res.templates:
                if tmpl not in self.resolver_map:
                    self.resolver_map[tmpl] = []
                self.resolver_map[tmpl].append(res)

    def compile_custom_initializers(self):
        """Map custom initializers by rule id."""
        self.initializer_map = {}
        for init in self.custom_initializers:
            rule = init.get("rule")
            if not rule:
                continue
            del init["rule"]
            if rule not in self.initializer_map:
                self.initializer_map[rule] = []
            self.initializer_map[rule].append(init)

    def apply_custom_initialization(self, rule_id, info, context):
        """Apply custom initialization templates for the given rule.

        Args:
            rule_id (str): The id of the matched rule
            info (dict): The info object to update
            context (dict): The current context
        """
        if rule_id in self.initializer_map:
            for init in self.initializer_map[rule_id]:
                if "where" in init:
                    if resolve_where_clause(init["where"], context):
                        logger.info(f"{rule_id} criteria fulfilled.")
                        apply_initializers(init["initialize"], info, context)
                    else:
                        continue

    def validate(self, templateDef, info):
        """Validate info against a template definition schema.

        Args:
            templateDef (dict): The template definition (schema)
            info (dict): The info object to validate

        Returns:
            list(string): A list of validation errors if invalid, otherwise an empty list.
        """
        if "_validator" not in templateDef:
            templateDef["_validator"] = jsonschema.Draft4Validator(templateDef)

        return list(sorted(templateDef["_validator"].iter_errors(info), key=str))

    def resolve_refs(self, resolver, obj, parent=None, key=None):
        """Resolve all references found in the definitions tree.

        Args:
            resolver (jsonschema.RefResolver): The resolver instance
            obj (object): The object to resolve
            parent (object): The parent object
            key: The key to the parent object
        """
        if isinstance(obj, dict):
            if parent and "$ref" in obj:
                ref, result = resolver.resolve(obj["$ref"])
                parent[key] = result
            else:
                for k in obj.keys():
                    self.resolve_refs(resolver, obj[k], obj, k)
        elif isinstance(obj, list):
            for i in range(len(obj)):
                self.resolve_refs(resolver, obj[i], obj, i)


class Rule:
    """Represents a matching rule for applying template definitions to resources or files within a project.

    Args:
        data (dict): The rule definition as a dictionary.

    Attributes:
        id (string): The optional rule id.
        template (str): The name of the template id to apply when this rule matches.
        initialize (dict): The optional set of initialization rules when this rule matches.
        conditions (dict): The set of conditions that must be true for this rule to match.
    """

    def __init__(self, data):
        self.id = data.get("id", "")
        self.template = data.get("template")
        self.initialize = data.get("initialize", {})
        if self.template is None:
            raise Exception('"template" field is required!')
        self.conditions = data.get("where")
        if not self.conditions:
            raise Exception('"where" field is required!')

    def test(self, context):
        """Test if the given context matches this rule.

        Args:
            context (dict): The context, which includes the hierarchy and current container

        Returns:
            bool: True if the rule matches the given context.
        """
        return resolve_where_clause(self.conditions, context)

    def initializeProperties(self, info, context):
        """Attempts to resolve initial values of BIDS fields from context.

        Template properties can now include an "initialize" field that
        gives instructions on how to attempt to initialize a field based
        on context. Within the initialize object, there are a list of
        keys to extract from the context, and currently regular expressions
        to match against the extracted fields. If the regex matches, then
        the "value" group will be extracted and assigned. Otherwise, if
        'take' is True for an initialization spec, we will copy that value
        into the field.

        Args:
            context (dict): The full context object
            info (dict): The BIDS data to update, if matched
        """
        apply_initializers(self.initialize, info, context)
        handle_run_counter_initializer(self.initialize, info, context)


def apply_initializers(initializers, info, context):
    """Attempts to resolve initial values of BIDS fields from context.

    In theory logging here only occurs on things that successfully
    match a BIDS template.

    Args:
        initializers (dict): The list of initializer specifications
        context (dict): The full context object
        info (dict): The BIDS data to update, if matched
    """
    for propName, propDef in initializers.items():
        resolvedValue = None

        if isinstance(propDef, dict):
            if "$switch" in propDef:
                resolvedValue = handle_switch_initializer(propDef["$switch"], context)
                if not resolvedValue:
                    logger.debug(f"Unable to match switch case {propDef['$switch']}")

            else:
                for key, valueSpec in propDef.items():
                    # Lookup the value of the key
                    value = utils.dict_lookup(context, key)
                    if value is not None:
                        # Regex matching must provide a 'value' group
                        if "$regex" in valueSpec:
                            regex_list = valueSpec["$regex"]
                            if not isinstance(regex_list, list):
                                regex_list = [regex_list]

                            for regex in regex_list:
                                # when searching, cast value as str, in case it's a list
                                m = re.search(regex, str(value))
                                if m is not None:
                                    resolvedValue = m.group("value")
                                    break
                            if m is None:
                                logger.debug(
                                    f"Unable to match regex <{regex_list}> to <{value}>"
                                )

                        # 'take' will just copy the value
                        elif "$take" in valueSpec and valueSpec["$take"]:
                            resolvedValue = value

                        if "$format" in valueSpec and resolvedValue:
                            resolvedValue = utils.format_value(
                                valueSpec["$format"], resolvedValue
                            )

                        if resolvedValue:
                            break

                    elif key == "$value":
                        resolvedValue = valueSpec

                    elif key != "$run_counter":  # run counters are handled later
                        logger.debug(
                            f"Metadata key <{key}> does not exist on this object"
                        )
        else:
            resolvedValue = propDef

        # Allows resolved value to be a blank string ""
        if resolvedValue is not None:
            info[propName] = resolvedValue


def handle_switch_initializer(switchDef, context):
    """Evaluate the switch statement on the context to return value."""

    def switch_regex_case(value, regex_pattern):
        result = re.match(regex_pattern, str(value))
        return bool(result)

    value = utils.dict_lookup(context, switchDef["$on"])
    logger.debug(f"value is {value}")
    if isinstance(value, list):
        value = set(value)

    comparators = {"$eq": operator.eq, "$regex": switch_regex_case, "$neq": operator.ne}

    for caseDef in switchDef["$cases"]:
        if "$default" in caseDef:
            return caseDef.get("$value")

        compOperation = None
        for comparator in comparators.keys():
            compValue = caseDef.get(comparator)
            if compValue:
                compOperation = comparators[comparator]
                break
        if isinstance(compValue, list):
            compValue = set(compValue)

        if compOperation:
            its_a_match = compOperation(value, compValue)
            if its_a_match:
                logger.debug(f'match for {compValue} : {caseDef.get("$value")}')
                return caseDef.get("$value")
            else:
                logger.debug(
                    f'no match for {compValue} for value {caseDef.get("$value")}'
                )

    if "$default" in caseDef:
        logger.debug(f'returning default {caseDef.get("$value")}')
        return caseDef.get("$value")

    return None


def handle_run_counter_initializer(initializers, info, context):
    counter_map = context.get("run_counters")
    if not counter_map:
        return

    for propName, propDef in initializers.items():
        if isinstance(propDef, dict) and "$run_counter" in propDef:
            current = info.get(propName)

            key = propDef["$run_counter"]["key"]
            key = utils.process_string_template(key, context)

            if current in ("+", "="):
                run_counter = counter_map[
                    key
                ]  # creates run_counter if it doesn't exist
                if current == "+":
                    info[propName] = run_counter.next()
                else:
                    info[propName] = run_counter.current()

            # This turns out to cause more trouble than it solved (auto-incrementing run counter
            #  if it was already used).
            # elif current.isdigit():
            #    run_counter = counter_map[
            #        key
            #    ]  # creates run_counter if it doesn't exist
            #    info[propName] = run_counter.increment_if_used(current)

            # else: if it is an empty or other string or some crazy thing, just use it as is
            # and don't create a run_counter


def resolve_where_clause(conditions, context):
    """Test if the given context matches this rule.

    A rule "where" clause consists of "conditions" (i.e. condition criteria below) or logical operators ("$and", "$or").
    Condition criteria are are dict key/value pairs like
      "container_type": "file",
      "file.name": { "$regex": "events\\.tsv$" },
      "file.type": { "$in": [ "tabular data", "Tabular Data", "source code", "JSON" ] },
    A dictionary of conditions are implicitly "and"ed together so "$and" is not actually necessary.

    Example of nested conditions:
      conditions = {
          "$or": [
              {
                  "file.type": {"$in": ["nifti", "NIfTI"]},
                  "$or": [
                      {"file.info.ImageType": {"$in": ["ORIGINAL"]}},
                      {"file.info.header.dicom.ImageType": {"$in": ["ORIGINAL"]}},
                  ],
              },
              {
                  "file.type": {"$in": ["dicom"]},
                  "$or": [
                      {"file.info.ImageType": {"$in": ["DERIVED"]}},
                      {"file.info.header.dicom.ImageType": {"$in": ["DERIVED"]}},
                  ],
              },
          ]
      }

    Args:
        conditions (dict): condition criteria or logical operators
        context (dict): The context, which includes the hierarchy and current container

    Returns:
        bool: True if the rule matches the given context.
    """
    for field, match in conditions.items():
        if "$" in field:  # then either $and or $or
            if isinstance(match, dict):  # $and, so treat like implicit and
                if not resolve_where_clause(match, context):
                    return False
            else:  # $or, so a list of conditions
                all_conditions_false = True
                for sub_match in match:
                    if resolve_where_clause(sub_match, context):
                        all_conditions_false = False
                        break
                if all_conditions_false:
                    return False
        else:  # a normal "condition" implicit and (if any are false, quit)
            value = utils.dict_lookup(context, field)
            if not processValueMatch(value, match, context, field):
                return False
    return True


def processValueMatch(value, match, context, condition=None):  # noqa PLR0911
    """Helper function that recursively performs value matching.

    Args:
        value: The value to match
        match: The matching rule
    Returns:
        bool: The result of matching the value against the match spec.
    """
    if condition in ("$or", "$and"):
        raise Exception("Code execution never gets here")

    if isinstance(match, dict):
        # Deeper processing
        if "$in" in match:
            # Check if value is in list
            if isinstance(value, list):
                for item in value:
                    if item in match["$in"]:
                        # logger.debug(f"Success: <{item}> matches <{match['$in']}>")
                        return True
                # logger.debug(f"Failed: {value} not in {match['$in']}")
                return False
            elif isinstance(value, six.string_types):
                for item in match["$in"]:
                    if item in value:
                        # logger.debug(f"Success: <{item}> matches <{match['$in']}>")
                        return True
                # logger.debug(f"Failed: <{value}> not in {match['$in']}")
                return False
            return value in match["$in"]

        elif "$not" in match:
            # Negate result of nested match
            return not processValueMatch(value, match["$not"], context)

        elif "$regex" in match:
            regex = re.compile(match["$regex"])

            if isinstance(value, list):
                for item in value:
                    if regex.search(str(item)) is not None:
                        # logger.debug(f"Success: <{item}> found in <{match['$regex']}>")
                        return True

                # logger.debug(f"Failed: No match for regex {regex}")
                return False

            if value is None:
                # logger.debug(f"Failed: No match for regex {regex}")
                return False

            return regex.search(str(value)) is not None

    else:
        if value == match:
            matched = True
        elif isinstance(value, list) and len(value) == 1 and value[0] == match:
            matched = True
        else:
            matched = False

        # if matched:
        #     logger.debug(f"Success: <{value}> matches <{match}>")
        # else:
        #     logger.debug(f"Failed: <{value}> does not match <{match}>")
        return matched


def load_template(path=None, template_name=None, save_sidecar_as_metadata=False):
    """Load the template at path or the named template at the default path.

    Args:
        fw (Flywheel Client)
        path (str): The path to the template to load
        template_name (str): will load default_path + / + template_name + .json
        save_sidecar_as_metadata (bool): sidecar info is stored in metadata not sidecar file
    Returns:
        Template: The template that was loaded (otherwise throws)
    """
    if path is None:
        if template_name is None:
            template_name = DEFAULT_TEMPLATE_NAME

        path = os.path.join(DEFAULT_TEMPLATE_DIR, template_name + ".json")

    logger.info("Using project curation template: '%s'", path)

    data = load_and_normalize_json(path)

    return Template(data, save_sidecar_as_metadata)
