/**
 * Node.js example using the compiled Python executable.
 * The executable is standalone - no Python or dependencies needed on the deployed machine!
 */

const { spawn } = require("child_process");
const path = require("path");

const projectRoot = path.join(__dirname);
const executablePath = path.join(projectRoot, "dist", "exe");
// On Windows, use: path.join(projectRoot, 'dist', 'exe.exe')

function predictPrice(area, modelPath = null) {
  return new Promise((resolve, reject) => {
    const args = [area.toString()];
    if (modelPath) {
      args.push(modelPath);
    }

    console.log("Spawning executable:", executablePath);
    // Spawn the standalone executable - no Python needed!
    const process = spawn(executablePath, args, {
      cwd: projectRoot,
      env: { ...process.env },
    });

    let stdout = "";
    let stderr = "";

    process.stdout.on("data", (data) => {
      stdout += data.toString();
    });

    process.stderr.on("data", (data) => {
      stderr += data.toString();
    });

    process.on("close", (code) => {
      if (code !== 0) {
        reject(
          new Error(
            `Process exited with code ${code}. Error: ${stderr || stdout}`
          )
        );
        return;
      }

      try {
        const result = JSON.parse(stdout);
        if (result.success) {
          resolve(result);
        } else {
          reject(new Error(result.error || "Prediction failed"));
        }
      } catch (error) {
        reject(
          new Error(`Failed to parse JSON: ${error.message}. Output: ${stdout}`)
        );
      }
    });

    process.on("error", (error) => {
      if (error.code === "ENOENT") {
        reject(
          new Error(
            `Executable not found at: ${executablePath}\nRun: python build.py to build it first.`
          )
        );
      } else {
        reject(new Error(`Failed to start process: ${error.message}`));
      }
    });
  });
}

// Example usage
async function main() {
  try {
    const result = await predictPrice(5000);
    console.log("Result:", result);
    console.log(`Predicted price: $${result.prediction.toFixed(2)}`);
  } catch (error) {
    console.error("Error:", error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { predictPrice };
