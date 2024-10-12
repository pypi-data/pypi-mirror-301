import os
from pathlib import Path
from Foundation import NSURL
from CoreML import MLModel, MLModelConfiguration, MLComputePlan
from PyObjCTools import AppHelper
import enum
from colorama import Fore, Style

class _ComputeDevice(enum.Enum):
    CPU = 0
    GPU = 1
    ANE = 2
    Unknown = 3

    def __str__(self):
        return self.name

    @classmethod
    def from_pyobjc(cls, device):
        from CoreML import MLCPUComputeDevice, MLGPUComputeDevice, MLNeuralEngineComputeDevice
        if isinstance(device, MLCPUComputeDevice):
            return cls.CPU
        elif isinstance(device, MLGPUComputeDevice):
            return cls.GPU
        elif isinstance(device, MLNeuralEngineComputeDevice):
            return cls.ANE
        else:
            return cls.Unknown

class CoreMLAnalyzer:
    def __init__(self):
        self.device_counts = {device: 0 for device in _ComputeDevice}
        self.total_operations = 0
        self.model_path = None

    def analyze(self, model_path):
        """Analyze the given CoreML model."""
        self._validate_and_prepare_model(model_path)
        self._run_analysis()
        return self.device_counts, self.total_operations

    def _validate_and_prepare_model(self, model_path):
        """Validate the model path and convert if necessary."""
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"File {model_path} does not exist")

        if model_path.endswith('.mlpackage'):
            self.model_path = self._convert_mlpackage_to_mlmodelc(model_path)
        elif model_path.endswith('.mlmodelc'):
            self.model_path = model_path
        else:
            raise ValueError("Input file must be either .mlpackage or .mlmodelc")

    def _convert_mlpackage_to_mlmodelc(self, input_path):
        """Convert .mlpackage to .mlmodelc."""
        url = NSURL.fileURLWithPath_(input_path)
        compiled_path, error = MLModel.compileModelAtURL_error_(url, None)
        if error:
            raise ValueError(f"Error compiling model: {error}")
        output_path = Path(input_path).with_suffix(".mlmodelc")
        Path(compiled_path).rename(output_path)
        return str(output_path)

    def _run_analysis(self):
        """Run the analysis on the prepared model."""
        config = MLModelConfiguration.alloc().init()
        MLComputePlan.loadContentsOfURL_configuration_completionHandler_(
            NSURL.fileURLWithPath_(self.model_path),
            config,
            self._handle_compute_plan
        )
        AppHelper.runConsoleEventLoop(installInterrupt=True)

    def _handle_compute_plan(self, compute_plan, error):
        """Handle the compute plan callback."""
        if error:
            raise RuntimeError(f"Error loading compute plan: {error}")
        
        if compute_plan:
            self._analyze_compute_plan(compute_plan)
        else:
            raise ValueError("No compute plan returned")
        
        AppHelper.callAfter(AppHelper.stopEventLoop)

    def _analyze_compute_plan(self, compute_plan):
        """Analyze the compute plan and update device counts."""
        program = compute_plan.modelStructure().program()
        if not program:
            raise ValueError("Missing program")
        
        main_function = program.functions().objectForKey_("main")
        if not main_function:
            raise ValueError("Missing main function")
        
        operations = main_function.block().operations()
        
        for operation in operations:
            device_usage = compute_plan.computeDeviceUsageForMLProgramOperation_(operation)
            if device_usage:
                device_type = _ComputeDevice.from_pyobjc(device_usage.preferredComputeDevice())
                self.device_counts[device_type] += 1
            self.total_operations += 1

    def create_bar_chart(self, total_width=50):
        """Create a bar chart representation of device counts."""
        total = sum(self.device_counts.values())
        title = "Compute Unit Mapping"
        bar = ""
        legend = f"All: {total}  "
        colors = {
            _ComputeDevice.CPU: Fore.BLUE,
            _ComputeDevice.GPU: Fore.GREEN,
            _ComputeDevice.ANE: Fore.MAGENTA,
            _ComputeDevice.Unknown: Fore.YELLOW
        }
        
        for device, count in self.device_counts.items():
            width = int(count / total * total_width) if total > 0 else 0
            bar += colors[device] + '█' * width
            legend += f"{colors[device]}■{Style.RESET_ALL} {device}: {count}  "

        return f"\033[1m{title}\033[0m\n{bar}{Style.RESET_ALL}\n{legend}"
