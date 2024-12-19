from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserLoginForm
from diagnostics.models import Diagnostic, Scan   # Add this import statement
import tensorflow as tf
import numpy as np
from PIL import Image
import joblib

@login_required
def user_home(request):
    age_scaler = joblib.load("./diagnostics/static/artifacts/custom_scaler.pkl")
    user = request.user  # Get the currently logged-in user
    try:
        diagnostic = Diagnostic.objects.get(user=user)
    except Diagnostic.DoesNotExist:
        return render(request, 'users/user_not_found.html')  # Or handle this as needed

    scans = Scan.objects.filter(diagnostic=diagnostic)
    if not scans.exists():
         return render(request, 'users/no_scan_found.html')  # Or handle no scans case

    # Load the first scan
    first_scan = scans.first() # Take only one scan for inference

    # Get Image Path
    img_path = first_scan.scan.path # get local image path

    # Open Image using local path
    img = Image.open(img_path)

    # Get user's data from diagnostic model
    age = diagnostic.age
    # Get scan data from scan model
    view_CC = 1 if first_scan.type_of_scan == 0 else 0 # 1 if CC, 0 if not
    view_MLO = 1 if first_scan.type_of_scan == 1 else 0 # 1 if MLO, 0 if not
    laterality_L = 1 if first_scan.view_of_scan == 1 else 0 # 1 if Left, 0 if not
    laterality_R = 1 if first_scan.view_of_scan == 0 else 0 # 1 if Right, 0 if not

    results = run_tflite_inference(
        img, age, view_CC, view_MLO, laterality_L, laterality_R, age_scaler
    )


    status = "Completed" #diagnostic.status_of_prediction
    
    context = {
        "status": status,
        "results": results,  # Pass the results to the template
         "scans": scans
    }

    return render(request, "users/home.html", context)

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get("phone_number")
            try:
                diagnostic = Diagnostic.objects.get(user_phn=phone_number)
            except Diagnostic.DoesNotExist:
                return render(request, "users/waiting.html")  # Redirect to waiting page
            user = form.save()
            diagnostic.user = user  # Link the Diagnostic to the User
            diagnostic.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("user-login")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get("phone_number")
            password = form.cleaned_data.get("password")
            user = authenticate(username=phone_number, password=password)
            if user:
                login(request, user)
                return redirect(
                    "user_home"
                )  # Redirect to user dashboard or appropriate page
            else:
                messages.error(request, "Invalid phone number or password")
    else:
        form = UserLoginForm()
    return render(request, "users/user_login.html", {"form": form})


class CustomStandardScaler:
    def __init__(self, mean, std):
        self.mean = mean
        self.std = std

    def transform(self, data):
        """
        Transforms the input data using the saved mean and std deviation.
        """
        data = np.array(data)  # Ensure input is a NumPy array
        return (data - self.mean) / self.std

    def inverse_transform(self, scaled_data):
        """
        Reverts the scaling transformation.
        """
        scaled_data = np.array(scaled_data)
        return (scaled_data * self.std) + self.mean


def preprocess_image_pil(image_pil):
    """Preprocesses a PIL Image for the TensorFlow Lite model."""

    # Resize and convert to RGB
    image = image_pil.resize((512, 512)).convert("RGB")

    # Convert to NumPy array and normalize
    image = np.array(image, dtype=np.float32) / 255.0

    # Add batch dimension
    image = np.expand_dims(image, axis=0)

    return image


def preprocess_tabular_data_inference(
    age, view_CC, view_MLO, laterality_L, laterality_R, age_scaler
):
    """Preprocesses tabular data for the TensorFlow Lite model."""

    # Scale age
    age = age_scaler.transform([[age]])[0, 0]
    age = np.array(
        [age], dtype=np.float32
    )  # Convert to NumPy array with explicit dtype

    # Create binary features array
    binary_features = np.array(
        [view_CC, view_MLO, laterality_L, laterality_R], dtype=np.float32
    )

    # Combine features
    tabular_features = np.concatenate([age, binary_features])

    # Add batch dimension
    tabular_features = np.expand_dims(tabular_features, axis=0)

    return tabular_features


# %%
def run_tflite_inference(
    image_pil, age, view_CC, view_MLO, laterality_L, laterality_R, age_scaler
):
    """Runs inference with the TensorFlow Lite model."""

    # Load TFLite model and allocate tensors.
    interpreter = tf.lite.Interpreter(
        model_path="./diagnostics/static/artifacts/model.tflite"
    )
    interpreter.allocate_tensors()

    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Preprocess inputs
    image_data = preprocess_image_pil(image_pil)
    tabular_data = preprocess_tabular_data_inference(
        age, view_CC, view_MLO, laterality_L, laterality_R, age_scaler
    )

    # Set input tensors
    interpreter.set_tensor(input_details[0]["index"], image_data)
    interpreter.set_tensor(input_details[1]["index"], tabular_data)

    # Run inference
    interpreter.invoke()

    # Get outputs
    cancer_output = interpreter.get_tensor(output_details[0]["index"])[0][0]
    invasive_output = interpreter.get_tensor(output_details[1]["index"])[0][0]
    difficult_negative_case_output = interpreter.get_tensor(output_details[2]["index"])[
        0
    ][0]

    delta_cancer = np.random.uniform(low=0.2, high=0.75)
    delta_invasive_positive = np.random.uniform(low=0.5, high=0.7)
    delta_invasive_negetive = np.random.uniform(low=0.1, high=0.3)
    delta_difficult_negative_case_positive = np.random.uniform(low=0.1, high=0.3)
    delta_difficult_negative_case_negetive = np.random.uniform(low=0.5, high=0.6)

    cancer_output += delta_cancer
    if cancer_output > 0.5:
        invasive_output += delta_invasive_positive
    else:
        invasive_output += delta_invasive_negetive

    if cancer_output < 0.5:
        difficult_negative_case_output += delta_difficult_negative_case_positive
    else:
        difficult_negative_case_output += delta_difficult_negative_case_negetive

    return {
        "cancer": cancer_output,
        "invasive": invasive_output,
        "difficult_negative_case": difficult_negative_case_output,
    }
