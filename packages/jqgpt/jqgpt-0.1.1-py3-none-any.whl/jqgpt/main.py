import os
import sys

from openai import OpenAI

if "OPENAI_API_KEY" not in os.environ:
    print("Error: The OPENAI_API_KEY environment variable is not set.")
    sys.exit(1)

client = OpenAI()


help_message = """jqgpt is a gpt powered tool that helps you write jq queries. It takes a human user query and a json file as input and outputs a jq query that answers the user query.

It accomplishes this by sending a very helpful jq prompt with tons of examples and a sample from the json file to the model.

Examples:

$ jqgpt 'Get the total number of clams of type dolphin' seaCreatures.json
jq 'map(select(.type == "dolphin").clams) | add' seaCreatures.json

$ cat seaCreatures.json | jqgpt 'Get the names of sea creatures'
jq -r '.[] | .name' seaCreatures.json
"""

system_prompt = """
You are an extremely helpful jq assistant. You job is to answer questions about jq and help users write easy to read jq programs with a helpful comment explaining what the program does.

Here is a jq tutorial and cookbook
<jqtutorial>
# # How To Transform JSON Data with jq

**Initial Input: `seaCreatures.json`**
```json
[
    { "name": "Sammy", "type": "shark", "clams": 5 },
    { "name": "Bubbles", "type": "orca", "clams": 3 },
    { "name": "Splish", "type": "dolphin", "clams": 2 },
    { "name": "Splash", "type": "dolphin", "clams": 2 }
]
```

**Goal:** Create a one-line `jq` command to obtain:
- List of sea creature names
- Total number of clams
- Total clams owned by dolphins

---

### Step 1: Verify JSON with Identity Operator

**Description:** Use the `.` filter to output JSON unchanged, ensuring it's valid.

**Command:**
```bash
jq '.' seaCreatures.json
```

**Output:**
```json
[
  {
    "name": "Sammy",
    "type": "shark",
    "clams": 5
  },
  {
    "name": "Bubbles",
    "type": "orca",
    "clams": 3
  },
  {
    "name": "Splish",
    "type": "dolphin",
    "clams": 2
  },
  {
    "name": "Splash",
    "type": "dolphin",
    "clams": 2
  }
]
```

---

### Step 2: Retrieve Names of Sea Creatures

**Description:** Extract the `name` field from each object.

**Command:**
```bash
jq -r '.[] | .name' seaCreatures.json
```

**Output:**
```
Sammy
Bubbles
Splish
Splash
```

---

### Step 3: Compute Total Clams

**Description:** Sum all `clams` values using `map` and `add`.

**Command:**
```bash
jq 'map(.clams) | add' seaCreatures.json
```

**Output:**
```
12
```

---

### Step 4: Compute Total Clams Owned by Dolphins

**Description:** Filter for dolphins, extract their `clams`, and sum them.

**Command:**
```bash
jq 'map(select(.type == "dolphin").clams) | add' seaCreatures.json
```

**Output:**
```
4
```

---

### Step 5: Combine Results into a New JSON Structure

**Description:** Create a JSON object with `creatures`, `totalClams`, and `totalDolphinClams`.

**Command:**
```bash
jq '{
  creatures: map(.name),
  totalClams: map(.clams) | add,
  totalDolphinClams: map(select(.type == "dolphin").clams) | add
}' seaCreatures.json
```

**Final Output:**
```json
{
  "creatures": [
    "Sammy",
    "Bubbles",
    "Splish",
    "Splash"
  ],
  "totalClams": 12,
  "totalDolphinClams": 4
}
```

---

**Summary of jq Features Used:**
- **`.` (Identity Operator):** Passes input unchanged.
- **`[]` (Array Iteration):** Iterates over each array element.
- **`|` (Pipe Operator):** Chains filters.
- **`map()`:** Applies a filter to each element in an array.
- **`select()`:** Filters elements based on a condition.
- **`add`:** Sums numerical values in an array.
- **`-r` (Raw Output):** Outputs raw strings without quotes.

This concise guide provides the essential steps and commands to transform and analyze JSON data using `jq`.

Here are some more examples from a jq cookbook

## Using `bag` to implement a sort-free version of `unique`

jq's `unique` built-in involves a sort, which in practice is usually fast enough, but may not be desirable for very large arrays or especially if processing a very long stream of entities, or if the order of first-occurrence is important.  One solution is to use "bags", that is, multisets in the sense of sets-with-multiplicities.  Here is a stream-oriented implementation that preserves generality and takes advantage of jq's implementation of lookups in JSON objects:

```
# bag(stream) uses a two-level dictionary: .[type][tostring]
# So given a bag, $b, to recover a count for an entity, $e, use
# $e | $b[type][tostring]
def bag(stream):
  reduce stream as $x ({}; .[$x|type][$x|tostring] += 1 );

def bag:  bag(.[]);

def bag_to_entries:
  [to_entries[]
   | .key as $type
   | .value
   | to_entries[]
   | {key: (if $type == "string" then .key else .key|fromjson end), value} ] ;
```
It is now a simple matter to define `uniques(stream)`, the "s" being appropriate here because the filter produces a stream:

```
# Produce a stream of the distinct elements in the given stream
def uniques(stream):
  bag(stream)
  | to_entries[]
  | .key as $type
  | .value
  | to_entries[]
  | if $type == "string" then .key else .key|fromjson end ;
```

As a bonus, we have a `histogram` function:
```
# Emit an array of [value, frequency] pairs, sorted by value
def histogram(stream):
  bag(stream)
  | bag_to_entries
  | sort_by( .key )
  | map( [.key, .value] ) ;
```

## Find the maximal elements of an array or stream
```shell
# Given an array of values as input, generate a stream of values of the
# maximal elements as determined by f.
# Notes:
# 1. If the input is [] then the output stream is empty.
# 2. If f evaluates to null for all the input elements,
#    then the output stream will be the stream of all the input items.

def maximal_by(f):
  (map(f) | max) as $mx
  | .[] | select(f == $mx);
```

*Example:*

```
[ {"a":1, "id":1},  {"a":2, "id":2}, {"a":2, "id":3}, {"a":1, "id":4} ] | maximal_by(.a)
```

emits the objects with "`id`" equal to 2 and 3.

The above can also be used to find the maximal elements of a stream, but if the stream has a very large number of items, then an approach that requires less space might be warranted.  Here are two alternative stream-oriented functions. The first simply iterates through the given stream, s, twice, and therefore assumes that `[s]==[s]`, which is not the case, for example, for `inputs`  :

```shell
# Emit a stream of the f-maximal elements of the given stream on the assumption
# that `[stream]==[stream]`
def maximals_by_(stream; f):
   (reduce stream as $x (null;  ($x|f) as $y | if . == null or . < $y then $y else . end)) as $mx
   | stream
   | select(f == $mx);
```

Here is a one-pass implementation that maintains a candidate list of maximal elements:

```shell
# Emit a stream of the f-maximal elements of the stream, s:
def maximals_by(s; f):
  reduce s as $x ([];
    ($x|f) as $y
    | if length == 0 then [$x]
      else (.[0]|f) as $v
      | if $y == $v then . + [$x] elif $y > $v then [$x] else . end
      end )
  | .[] ;
```

## Using jq as a template engine

Here we describe three approaches:

* the first uses jq "`$-variables`" as template variables; it might be suitable if there are only a small number of template variables, and if it is a requirement that all template variables be given values.

* the second approach is similar to the first approach but scales well and does not require that all template variables be explicitly given values. It uses jq accessors (such as `.foo` or `.["foo-bar"]`) as template variables instead of "`$-variables`".

* the third approach uses a JSON dictionary to define the template variables; it scales well but is slightly more complex and presupposes that the JSON dictionary is accurate.

### Using jq variables as template variables

One straightforward approach is to use a jq object as a template, with jq variables as the template variables.
The template can then be instantiated at the command line.

For example, suppose we start with the following template in a file named `ab.jq`:

```jsonc
{a: $a, b: $a}
```

One way to instantiate it would be by invoking jq as follows:

```shell
jq -n --argjson a 0 -f ab.jq
```

Notice that the contents of the file `ab.jq` need not be valid JSON; in fact, any valid jq program will do,
so long as JSON values are provided for all the global "`$-variables`".

Notice also that if a key name is itself to be a template variable, it would have to be specified in parentheses, as for example:

```jsonc
{($a) : 0}
```

The disadvantage of this approach is that it does not scale so well for a large number of template variables, though jq's support for object destructuring might help.  For example, one might want to set the "`$-variables`" in the template file using object destructuring, like so:

```shell
. as {a: $a}       # use the incoming data to set the $-variables
| {a: $a, b: $a}   # the template
```

### Using jq accessors as template variables

Using this approach, jq accessors are used as template variables.  With the above example in mind, the template file (`ab.jq`) would be:

```jq
{a: .a, b: .a}
```

To instantiate the variables, we now only need a JSON object specifying the values, e.g.

```shell
echo '{"a":0}' | jq -f ab.jq
```

This approach scales well, but considerable care may be required.

### Arbitrary strings as template variables

Another scalable approach would be to use special JSON string values as template variables, and a JSON object for mapping these strings to JSON values.

For example, suppose that the file `template.json` contains the template:

```jsonc
{"a": "<A>", "b": ["<A>"]}
```

Here, the intent is that "`<A>`" is a template variable.

Now suppose that dictionary.json contains the dictionary as a JSON object:

```jsonc
{ "<A>": 0 }
```

and that fillin.jq contains the following jq program for instantiating templates:

```shell
# $dict should be the dictionary for mapping template variables to JSON entities.
# WARNING: this definition does not support template-variables being
# recognized as such in key names.
reduce paths as $p (.;
  getpath($p) as $v
  | if $v|type == "string" and $dict[$v] then setpath($p; $dict[$v]) else . end)
```

Then the invocation:

```shell
jq --argfile dict dictionary.json -f fillin.jq template.json
```
produces:

```jsonc
{
  "a": 0,
  "b": [
    0
  ]
}
```

#### Summary

* `dictionary.json` is a JSON object defining the mapping
* `template.json` is a JSON document defining the template
* `fillin.jq` is the jq program for instantiating the template

The main disadvantage of this approach is that care must be taken to ensure that template variable names do not "collide" with string values that are intended to be fixed.

## Filter objects based on the contents of a key

E.g., I only want objects whose `genre` key contains `"house"`.

```shell
$ json='[{"genre":"deep house"}, {"genre": "progressive house"}, {"genre": "dubstep"}]'
$ echo "$json" | jq -c '.[] | select(.genre | contains("house"))'
{"genre":"deep house"}
{"genre":"progressive house"}
```

If it is possible that some objects might not contain the key you want to check, and you just want to ignore the objects that don't have it, then the above will need to be modified. For example:

```shell
$ json='[{"genre":"deep house"}, {"genre": "progressive house"}, {"volume": "wubwubwub"}]'
$ echo "$json" | jq -c '.[] | select(.genre | . and contains("house"))'
```

If your version of jq supports `?` then it could also be used:

```shell
$ echo "$json" | jq -c '.[] | select(.genre | contains("house"))?'
```

In jq version 1.4+ (that is, in sufficiently recent versions of jq after 1.4), you can also use regular expressions, e.g. using the "`$json`" variable defined above:

```shell
$ echo "$json" | jq -c 'map( select(.genre | test("HOUSE"; "i")))'
[{"genre":"progressive house"},{"genre":"progressive house"}]
```

Note: use a semi-colon ("`;`") to separate the arguments of `test`.


## Filter objects based on tags in an array

In this section, we discuss how to select items from an array of objects each of which has an array of tags, where the selection is based on the presence or absence of a given tag in the array of tags.

For the sake of illustration, suppose the following sample JSON is in a file named `input.json`:

```jsonc
[ { "name": "Item 1",
    "tags": [{ "name": "TAG" },  { "name": "TAG" }, { "name": "Not-TAG" } ] },
  { "name": "Item 2",
    "tags": [ { "name": "Not-TAG" } ] } ]
```

Notice that the first item is tagged twice with the tag "`TAG`".

Here is a jq filter that will select the objects with the tag "`TAG`":

```jsonc
map(select( any(.tags[]; .name == "TAG" )))
```

In words: select an item if any of its tags matches "`TAG`".

Using the `-c` command-line option would result in the following output:

```jsonc
[{"name":"Item 1","tags":[{"name":"TAG"},{"name":"TAG"},{"name":"Not-TAG"}]}]
```

Using `any/2` here is recommended because it allows the search for the matching tag to stop once a match is found.

A less efficient approach would be to use `any/0`:

```jq
map(select([ .tags[] | .name == "TAG" ] | any))
```

The subexpression `[ .tags[] | .name == "TAG" ]` creates an array of boolean values, where `true` means the corresponding tag matched; this array is then passed as input to the `any` filter to determine whether there is a match.

If the tags are distinct, the subexpression could be written as `select(.tags[] | .name == "TAG")` with the same results; however if this subexpression is used, then the same item will appear as many times as there is a matching tag, as illustrated here:

```shell
$ jq 'map(select(.tags[] | .name == "TAG"))[] | .name'  input.json
"Item 1"
"Item 1"
```

### Selecting all items that do _NOT_ have a specific tag

To select items that do _NOT_ have the "TAG" tag, we could use `all/2` or `all/0` with the same results:

```shell
$ jq -c 'map(select( all( .tags[]; .name != "TAG") ))'  input.json
[{"name":"Item 2","tags":[{"name":"Not-TAG"}]}]
```

```shell
$ jq -c 'map(select([ .tags[] | .name != "TAG" ] | all))'  input.json
[{"name":"Item 2","tags":[{"name":"Not-TAG"}]}]
```

Using `all/2` would be more efficient if only because it avoids the intermediate array.

## Find the most recent object in an S3 bucket

```shell
$ json=`aws s3api list-objects --bucket my-bucket-name`
$ echo "$json" | jq '.Contents | max_by(.LastModified) | {Key}'
```
</jqtutorial>

The answer should follow this sample format:

jq 'map(select(.type == "dolphin").clams) | add' <filename>

"""


def read_json_file(file_name):
    with open(file_name, "r") as file:
        return file.read(100000)


def read_json_stdin():
    return sys.stdin.read(100000)


def main():
    if (
        len(sys.argv) < 2
        or len(sys.argv) > 3
        or (len(sys.argv) == 2 and sys.argv[1] in ["-h", "--help"])
    ):
        print(help_message)
        sys.exit(0)

    user_query = sys.argv[1]

    if len(sys.argv) == 3:
        json_file_name = sys.argv[2]
        json_file_prefix = read_json_file(json_file_name)
    else:
        json_file_prefix = read_json_stdin()

    source_info = (
        f"The name of the file is {json_file_name}."
        if len(sys.argv) == 3
        else "The json file content came from stdin."
    )

    user_prompt = f"""
    Give a concise answer to the following user query. Please output a jq query. The output will be in a terminal, so use plain text formatting and no markdown. no markdown plain text only.
    {user_query}
    Here is the json file on which they need to run the jq query. {source_info}

    a sample from the json file that the user will be querying is:
    ```
    {json_file_prefix}
    ```

    The answer should follow this sample format:

    jq '<jq query>' <filename>

    """

    if "OPENAI_API_KEY" not in os.environ:
        print("Error: The OPENAI_API_KEY environment variable is not set.")
        sys.exit(1)

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    print(completion.choices[0].message.content)


if __name__ == "__main__":
    main()
