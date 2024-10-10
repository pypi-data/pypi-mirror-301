# VIPAS AI Platform SDK
The Vipas AI Python SDK provides a simple and intuitive interface to interact with the Vipas AI platform. This SDK allows you to easily make predictions using pre-trained models hosted on the Vipas AI platform.

## Requirements.

Python 3.7+

## Installation & Usage
### pip install

You can install vipas sdk from the pip repository, using the following command:

```sh
pip install vipas
```
(you may need to run `pip` with root permission: `sudo pip install vipas`)

Then import the package:
```python
import vipas
```
## Prerequisites
Before using the Vipas.AI SDK to manage and publish models, you need to fetch your VPS Auth Token from the Vipas.AI platform and configure it as an environment variable.

#### Step 1: Fetching the Auth Token:-
1. Login to Vipas.AI: Go to the [Vipas.AI](https://vipas.ai) platform and log in to your account.
2. Navigate to Settings: Click on your user profile icon in the top right corner and navigate to Settings.
Generate Auth Token: In the settings, locate the **Temporary Access Token** section, enter your password. 
3. Click the button to generate a new Auth Token.
Copy the Token: Once generated, copy the token. This token is required to authenticate your SDK requests.

#### Step 2: Setting the Auth Token as an Environment Variable:-
You need to set the VPS_AUTH_TOKEN as an environment variable to use it within your SDK.

##### For linux and macOS
1. Open a **Terminal**.
2. Run the following command to export the token:

    ```bash
    export VPS_AUTH_TOKEN=<TOKEN>
    ```
   Replace <TOKEN> with the actual token you copied from the Vipas.AI UI.
3. To make it persistent across sessions, add the following line to your **~/.bashrc, ~/.zshrc**, or the corresponding shell configuration file

    ```bash
    export VPS_AUTH_TOKEN=<TOKEN>
    ```
    Then use this command to source it to the current running 
    session
    ```bash
    source ~/.bashrc.
    ```
##### For Windows
1. Open **Command Prompt** or **PowerShell**.
2. Run the following command to set the token for the current session:
    ```powershell
    set VPS_AUTH_TOKEN=<TOKEN>
    ```
3. To set it permanently, follow these steps:
    1. Open the Start menu, search for **Environment Variables**, and open the **Edit the system environment variables** option.
    2. In the **System Properties** window, click on **Environment Variables**.
    3. Under **User variables**, click **New**.
    4. Set the **Variable name** to **VPS_AUTH_TOKEN** and the Variable value to <TOKEN>.
    5. Click **OK** to save.

Once you’ve set the environment variable, you can proceed with using the SDK, as it will automatically pick up the token from the environment for authentication.





## Getting Started

To get started with the Vipas AI Python SDK, you need to create a ModelClient object and use it to make predictions. Below is a step-by-step guide on how to do this.

### Basic Usage

1. Import the necessary modules:
```python
from vipas import model
```

2. Create a ModelClient object:
```python
vps_model_client = model.ModelClient()
```

3. Make a prediction:

```python
model_id = "<MODEL_ID>"
api_response = vps_model_client.predict(model_id=model_id, input_data="<INPUT_DATA>")
```

### Handling Exceptions
The SDK provides specific exceptions to handle different error scenarios:

1. UnauthorizedException: Raised when the API key is invalid or missing.
2. NotFoundException: Raised when the model is not found.
3. BadRequestException: Raised when the input data is invalid.
4. ForbiddenException: Raised when the user does not have permission to access the model.
5. ConnectionException: Raised when there is a connection error.
6. RateLimitException: Raised when the rate limit is exceeded.
7. ClientException: Raised when there is a client error.

### Asynchronous Inference Mode
---
Asynchronous Inference Mode is a near-real-time inference option that queues incoming requests and processes them asynchronously. This mode is suitable when you need to handle `large payloads` as they arrive or run models with long inference processing times that do not require sub-second latency. `By default, the predict method operates in asynchronous mode`, which will poll the status endpoint until the result is ready. This is ideal for batch processing or tasks where immediate responses are not critical.


#### Asynchronous Inference Mode Example
```python
api_response = vps_model_client.predict(model_id=model_id, input_data="<INPUT_DATA>", async_mode=True)
```
### Real-Time Inference Mode
---
Real-Time Inference Mode is designed for use cases requiring real-time predictions. In this mode, the predict method processes the request immediately and returns the result without polling the status endpoint. This mode is ideal for applications that need quick, real-time responses and can afford to handle potential timeouts for long-running inferences. It is particularly suitable for interactive applications where users expect immediate feedback.

#### Real-Time Inference Mode Example
```python
api_response = vps_model_client.predict(model_id=model_id, input_data="<INPUT_DATA>", async_mode=False)
```

### Detailed Explanation
#### Asynchronous Inference Mode
---
##### Description:
This mode allows the system to handle requests by queuing them and processing them as resources become available. It is beneficial for scenarios where the inference task might take longer to process, and an immediate response is not necessary.

##### Behavior:
The system polls the status endpoint to check if the result is ready and returns the result once processing is complete.

##### Ideal For:
Batch processing, large payloads, long-running inference tasks.

##### Default Setting:
By default, async_mode is set to True to support heavier inference requests.

##### Example Usage:

```python
api_response = vps_model_client.predict(model_id=model_id, input_data="<INPUT_DATA>", async_mode=True)
```

#### Real-Time Inference Mode
---
##### Description:
This mode is intended for use cases that require immediate results. The system processes the request directly and returns the result without polling.

##### Behavior:
The request is processed immediately, and the result is returned. If the inference takes longer than 29 seconds, a 504 Gateway Timeout error is returned.

##### Ideal For:
Applications requiring sub-second latency, interactive applications needing immediate feedback.

##### Example Usage:

```python
api_response = vps_model_client.predict(model_id=model_id, input_data="<INPUT_DATA>", async_mode=False)
```

By understanding and choosing the appropriate mode for your use case, you can optimize the performance and responsiveness of your AI applications on Vipas.AI.


### Example Usage for ModelClient using asychronous inference mode

```python
from vipas import model
from vipas.exceptions import UnauthorizedException, NotFoundException, ClientException
from vipas.logger import LoggerClient

logger = LoggerClient(__name__)

def main():
    # Create a ModelClient object
    vps_model_client = model.ModelClient()

    # Make a prediction
    try:
        model_id = "<MODEL_ID>"
        api_response = vps_model_client.predict(model_id=model_id, input_data="<INPUT_DATA>")
        logger.info(f"Prediction response: {api_response}")
    except UnauthorizedException as err:
        logger.error(f"UnauthorizedException: {err}")
    except NotFoundException as err:
        logger.error(f"NotFoundException: {err}")
    except ClientException as err:
        logger.error(f"ClientException: {err}")

main()

```
## Publishing Model
The Vipas.AI SDK provides a simple and powerful interface for developers to publish, manage, and deploy AI models. With this SDK, developers can upload their models, configure model processors, and deploy them to the Vipas platform seamlessly. This documentation will guide you through the process of using the SDK to publish and manage models built on various machine learning frameworks, including TensorFlow, PyTorch, ONNX, XGBoost, Scikit-learn, and more.


### Getting Started
---
Here is a basic example of how to use the SDK to publish a model from any remote environment:

```python
from vipas.model import ModelClient
from vipas.exceptions import UnauthorizedException, NotFoundException, ClientException


# Paths to model and processor files
model_folder_path = "/path/to/your/model"
onnx_config_path = "/path/to/config/config.pbtxt"  # Optional, depends on framework
processor_folder_path = "/path/to/your/processor"

# Unique model ID to identify the model in Vipas.AI
model_id = "your_model_id" # mdl-xxxxxxxxx

try:
    # Initialize the ModelClient
    model_client = ModelClient()

    # Publish the model
    model_client.publish(
        model_id=model_id,
        model_folder_path=model_folder_path,
        model_framework_type="tensorflow",  # Supported: tensorflow, pytorch, onnx, xgboost, sklearn, etc.
        onnx_config_path=onnx_config_path,  # Required for the ONNX model framework        
        processor_folder_path=processor_folder_path,  # Optional if using custom processors
        processor_image="your-processor-image:latest",  # allowed value are [“vps-processor-base:1.0”]
        auto_launch=True,  # Whether to automatically launch the model after upload, Default True
        override_model=True  # Whether to override existing model deployments, Default True
    )
except UnauthorizedException as e:
    print(f"UnauthorizedException: {e}")
except NotFoundException as e:
    print(f"NotFoundException: {e}")
except ClientException as e:
    print(f"ClientException: {e}")
except Exception as e:
    print(f"Exception: {e}")
```

### Publishing Process Overview
---
When you publish a model using the Vipas SDK, the following steps occur behind the scenes:
1. **Model Upload**: The SDK uploads the model files from the specified directory. The total size of the files is calculated, and the upload process is logged step-by-step.
2. **Processor Upload (Optional)**: If you are using a custom processor (a custom Python script), the SDK uploads the processor files. This step is optional but can be critical for advanced use cases where model input needs specific transformations.
3. **Processor Staging(Optional)**: After the processor upload, the processor will get staged if the files are properly uploaded.
4. **Model Staging And Building Processor**: Once the model and its associated files (including the processor, if applicable) are uploaded, the model is placed in a staging state. This stage ensures that all files are correctly uploaded and prepares the model for deployment.
5. **Model Launch (Optional)**: If the auto_launch parameter is set to True, the model will be automatically launched. This means that the model will be deployed and become available for real-time and asynchronous inference. The launch status is logged until the process is completed successfully.
6. **Rollback Mechanism**: If a model is already deployed and a new version is being uploaded, the SDK ensures that the previous version is rolled back in case of any issues during the new model deployment. 
> **Note:** The Rollback Mechanism will not occur if you make override_model=False.

#### Key parameters
1. **model_id**: The unique identifier for the model. This ID is used to track the model across the platform.
2. **model_folder_path**: The path to the directory containing the model files that need to be uploaded.
3. **model_framework_type**: The framework used for the model (e.g., TensorFlow, PyTorch, ONNX, XGBoost, Scikit-learn). Each framework has its own nuances in terms of model configuration.
4. **onnx_config_path**: The path to the ONNX configuration file required by the ONNX framework. 
5. **processor_folder_path**: The path to the folder containing custom processor files, such as Python scripts, if applicable. Optional if using a processor.
6. **processor_image**: The Docker base image for the processor. Currently supporting “vps-processor-base:1.0”.
7. **auto_launch**: A boolean flag indicating whether to automatically launch the model after publishing. Default is True.
8. **override_model**: A boolean flag indicating whether to override any existing model deployment. Default is True.

#### Supported Frameworks
The SDK supports the following machine learning frameworks:
1. TensorFlow: Native TensorFlow SavedModel format.
2. PyTorch: Model files saved as .pt or .pth.
3. ONNX: ONNX models typically require a configuration file with extensions like (.pbtxt, .config, .txt) for setting input and output shapes.
4. XGBoost: For tree-based models exported from XGBoost.
5. Scikit-learn: For traditional machine learning models exported from scikit-learn.

> ⚠️ **Note:** For ONNX models, you must provide an ONNX configuration file with extensions like `.pbtxt`, `.config`, or `.txt` that describe the input-output mapping.
> 
> Below is an example ONNX configuration for input and output details needed by the model:
> 
> ```yaml
> input [
>  {
>    name: "input1"  # Name of the input going to the model (input tensor)
>    data_type: TYPE_FP32  # Data type of the input, FP32 stands for 32-bit floating point (commonly used in deep learning)
>    dims: [1, 3, 224, 224]  # Dimensions of the input tensor: [Batch size, Channels, Height, Width]
>  }
> ]
> output [
>  {
>    name: "output1"  # Name of the output from the model (output tensor)
>    data_type: TYPE_FP32  # Data type of the output, FP32 represents 32-bit floating point
>    dims: [1, 3, 224, 224]  # Dimensions of the output tensor: [Batch size, Channels, Height, Width]
>  }
> ]
> ```

#### Expected Behavior
1. **Successful Upload**: The model and processor files will be uploaded, and the model will be placed in the staged state.
2. **Automatic Launch**: If auto_launch=True, the model will be launched after the upload completes, making it available for real-time and asynchronous inference.
3. **Override of Existing Models**: If a model with the same model_id is already deployed, the new model will override the previous deployment if override_model=True.

#### Logs Example
Once you run the publish() method, you can expect logs similar to the following:
```bash
2024-10-08 16:15:15,043 - vipas.model - INFO - Publishing model mdl-ikas2ot2ohsux with framework type onnx.
2024-10-08 16:15:19,818 - vipas.model - INFO - File processor.py uploaded successfully.
2024-10-08 16:16:22,952 - vipas.model - INFO - Model mdl-ikas2ot2ohsux and related processor launched successfully.
```

This log sequence shows the entire process of publishing the model, uploading the processor, and successfully launching the model. Any errors or warnings will also be captured in the logs, which can help troubleshoot issues.




## Logging
The SDK provides a LoggerClient class to handle logging. Here's how you can use it:

### LoggerClient Usage

1. Import the `LoggerClient` class:
```python
from vipas.logger import LoggerClient
```

2. Initialize the `LoggerClient`:
```python
logger = LoggerClient(__name__)
```

3. Log messages at different levels:
```python
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")

```

### Example of LoggerClient
Here is a complete example demonstrating the usage of the LoggerClient:

```python
from vipas.logger import LoggerClient

def main():
    logger = LoggerClient(__name__)
    
    logger.info("Starting the main function")
    
    try:
        # Example operation
        result = 10 / 2
        logger.debug(f"Result of division: {result}")
    except ZeroDivisionError as e:
        logger.error("Error occurred: Division by zero")
    except Exception as e:
        logger.critical(f"Unexpected error: {str(e)}")
    finally:
        logger.info("End of the main function")

main()
``` 

## Author
VIPAS.AI

## License
This project is licensed under the terms of the [vipas.ai license](LICENSE.md).

By following the above guidelines, you can effectively use the VIPAS AI Python SDK to interact with the VIPAS AI platform for making predictions, handling exceptions, and logging activities.




