# Bladed Next Gen Python Models API

`dnv_bladed_models=0.4.1`

A Python package to easily work with JSON input models for Bladed Next Generation.

Visit <https://bladednextgen.dnv.com/> for more information.

## Prerequisites

- Requires Python 3.7 or above

## Usage

## Add import

```python
import dnv_bladed_models as models
```

There are a large number of model classes (500+) in the Bladed NG input API. They are all accessible via the `models` module.

The root model is `BladedAnalysis`; a JSON file input to the calculation engine must have this model as the root object.

However the same capabilities are available for every model; each one can be read and written to JSON individually, as demonstrated below.

### Load a full Bladed NG JSON analysis model from file

```python
analysis = models.BladedAnalysis.from_file('/path/to/analysis.json')
```

This will perform some validation of the input to ensure the structure adheres to the input model schema.

### Save a model to a JSON file

```python
analysis.to_file('/path/to/file.json')
```

The JSON file can then be opened in VS Code, and will automatically receive validation, doc-string and auto-complete support against the Bladed NG JSON Schema.

### Load a model from a JSON string

```python
analysis = models.BladedAnalysis.from_json(json_str)
```

This will perform some validation of the input to ensure the structure adheres to the input model schema.

### Render a model as a JSON string

```python
json_str = analysis.to_json()
```

### Create a new model object in code

Create a new instance of the root model, 'BladedAnalysis':

```python
analysis = models.BladedAnalysis()
```

A model object can be created with an empty initialiser as shown above, or by specifying some or all of the child models as keyword arguments:

```python
beam = models.LidarBeam(
    MountingPosition=models.LidarMountingPosition(
        X=1,
        Y=2,
        Z=3
    )
)
```

### Modify a model object in code

If a model object is already loaded, properties can be modified as required:

```python
analysis.SteadyCalculation.TipSpeedRatioRange.Minimum = 4.
analysis.SteadyCalculation.TipSpeedRatioRange.Maximum = 10.
analysis.SteadyCalculation.TipSpeedRatioRange.Interval = 0.1
```

### Manipulate the turbine assembly

Access existing component definitions:

```python
# Access a known existing component by it's key
blade: models.Blade = analysis.ComponentDefinitions['blade']

# Iterate over all component entries...
for key, component in analysis.ComponentDefinitions.items():
    print(f"Component key: {key}, Component type: {component.ComponentType}")

# Or just the keys
for key in analysis.ComponentDefinitions.keys():
    print(key)

# Or just the components
for component in analysis.ComponentDefinitions.values():
    print(component.ComponentType)
```

Access existing nodes in the Assembly tree using string and integer accessors:

```python
blade_node = analysis.Turbine.Assembly['hub']['pitch-system-1'][0]
# or
blade_node = analysis.Turbine.Assembly['hub']['pitch-system-1']['blade-1']
# or
blade_nodes = [ps_node[0] for node_name, ps_node in analysis.Turbine.Assembly['hub'].items()]
```

Add new nodes and component definitions:

```python
analysis.ComponentDefinitions['my-hub'] = models.IndependentPitchHub()
analysis.ComponentDefinitions['my-pitch-system'] = models.PitchSystem()
analysis.ComponentDefinitions['my-blade'] = models.Blade()

hub_node = models.AssemblyNode(
    ComponentReference = "#/ComponentDefinitions/my-hub"
)
for i in range(1,4):
    blade_node = models.AssemblyNode(
        ComponentReference = "#/ComponentDefinitions/my-blade"
    )
    ps_node = models.AssemblyNode(
        ComponentReference = "#/ComponentDefinitions/my-pitch-system"
    )
    ps_node[f'blade-{i}'] = blade_node
    hub_node[f'pitch-system-{i}'] = ps_node
analysis.Turbine.Assembly['hub'] = hub_node
```

### Change a model to an alternative choice

Some model properties can be set to one of a number of different model types, to allow a choice between different options available in the calculation.

The property must simply be set to an object of one of the valid types. The valid types available are included in the doc strings, and the schema documentation available on the Bladed Next Gen website.

The example below is for dynamic stall. The detail of setting the specific properties on each model is omitted for brevity:

```python
analysis.Aerodynamics.DynamicStall = models.OyeModel()

# or
analysis.Aerodynamics.DynamicStall = models.IAGModel()

# or
analysis.Aerodynamics.DynamicStall = models.CompressibleBeddoesLeishmanModel()

# or
analysis.Aerodynamics.DynamicStall = models.IncompressibleBeddoesLeishmanModel()
```
