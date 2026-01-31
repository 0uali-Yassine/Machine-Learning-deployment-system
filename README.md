# Python Model Predictor Standalone Executable

Standalone Python executable for building and using a trained model.
Can be called from Node.js or from the command line, in any machine.
Without any dependencies or Python installation.

## How It Works

- `src/build_executable.py` - Simple build script (no spec file needed!)
- Uses `--collect-all sklearn` to automatically bundle all sklearn dependencies
- Model is bundled into the executable
- Resulting executable is completely standalone - no Python or dependencies installation needed

## Step 1: Build

Build the standalone executable (no Python needed on deployed machine):

```bash
python src/build_executable.py
# or
uv run src/build_executable.py
```

This creates `dist/exe` - a standalone executable that includes Python and all dependencies.

## Step 2: Usage From Command Line

Make a prediction using the bundled model (only argument is the area):

```bash
./dist/exe 5000
```

Or with custom model path: (optional, if not provided, the bundled model will be used)

```bash
./dist/exe 5000 /path/to/model
```

### Step 3: Usage From Node.js

See `src/nodejs_example.js` for how to call the executable from Node.js.

```javascript
const { predictPrice } = require("./src/nodejs_example.js");

const result = await predictPrice(5000);
console.log("Result:", result);
console.log(`Predicted price: $${result.prediction.toFixed(2)}`);
```
