using System.Collections;
using Unity.Collections;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.XR.ARFoundation;
using UnityEngine.XR.ARSubsystems;
using UnityEngine.Networking;
using TMPro;

public class UI : MonoBehaviour
{
    public GameObject startButton; // Just a start button that will hide the greetings canvas
    public GameObject captureButton;
    public GameObject exitButton;
    public GameObject readMoreButton;
    public GameObject[] greetingCanvas; // All the game objects from the greeting canvas that need to be hidden later
    public GameObject avatar; // Access the avatar
    public RectTransform avatarTransform; // Used to make the avatar smaller
    public Vector2 bottomLeftAnchorPos;

    // Taking picture snapshot
    public ARCameraManager cameraManager;
    public RawImage previewImage;
    public GameObject previewImageObj;

    public GameObject resultTextObj;
    public TextMeshProUGUI resultText;

    [System.Serializable]
    public class Detection
    {
        public string @class;
        public float confidence;
        public float[] bbox;
        public string color;
        public string name;
    }

    [System.Serializable]
    public class DetectionResponse
    {
        public Detection[] detections;
    }

    [System.Serializable]
    public class DescriptionResponse
    {
        public string description;
    }


    // Start is called before the first frame update
    void Start()
    {
        // Set all buttons inactive for the initial log
        captureButton.SetActive(false); // Button to capture the picture initially inactive
        exitButton.SetActive(false); // Exit button to turn off the already taken picture
        readMoreButton.SetActive(false); // Button to read more about the picture
        previewImageObj.SetActive(false); // Picture preview of the taken picture
        resultTextObj.SetActive(false); // The result text that comes from the model

        // Assign functions to each button
        startButton.GetComponent<Button>().onClick.AddListener(OnStartClicked);
        captureButton.GetComponent<Button>().onClick.AddListener(OnCaptureButtonClicked);
        exitButton.GetComponent<Button>().onClick.AddListener(OnExitClicked);
        readMoreButton.GetComponent<Button>().onClick.AddListener(OnReadMoreClicked);
    }

    public void OnStartClicked()
    {
        // Hide intro elements
        startButton.SetActive(false);
        captureButton.SetActive(true);

        foreach (var obj in greetingCanvas)
        {
            obj.SetActive(false);
        }

        // Move avatar to bottom left
        if (avatarTransform != null)
        {
            avatarTransform.anchoredPosition = bottomLeftAnchorPos;
        }
        else
        {
            avatar.transform.position = Camera.main.ViewportToWorldPoint(new Vector3(0.1f, 0.1f, 1f)); // if it's not UI
        }

        // Enable avatar
        avatar.SetActive(true);

    }
    
    public void OnExitClicked()
    {
        previewImageObj.SetActive(false);
        readMoreButton.SetActive(false);
        exitButton.SetActive(false);
        resultTextObj.SetActive(false);
    }

    public void OnReadMoreClicked()
    {
        StartCoroutine(SendDescriptionRequest(resultText.text));
    }

    // Function to handle button click
    public void OnCaptureButtonClicked()
    {
        UnityEngine.Debug.Log("Button clicked!");

        // Capture the image from the AR camera
        CaptureCameraImage();
        previewImageObj.SetActive(true);
        exitButton.SetActive(true);

    }

    IEnumerator SendDescriptionRequest(string textContent)
    {
        UnityEngine.Debug.Log("Sending description request for: " + textContent);

        // Convert string to byte array (simulating a file upload)
        byte[] textBytes = System.Text.Encoding.UTF8.GetBytes(textContent);

        WWWForm form = new WWWForm();
        form.AddBinaryData("file", textBytes, "text.txt", "text/plain");

        using (UnityWebRequest www = UnityWebRequest.Post("http://192.168.197.97:8000/description/", form))
        {
            yield return www.SendWebRequest();

            if (www.result == UnityWebRequest.Result.Success)
            {
                string json = www.downloadHandler.text;
                DescriptionResponse response = JsonUtility.FromJson<DescriptionResponse>(json);

                if (!string.IsNullOrEmpty(response.description))
                {
                    resultText.text = response.description;
                }
                else
                {
                    resultText.text = resultText.text;
                    UnityEngine.Debug.Log("Description was empty, keeping previous text.");
                }
            }
            else
            {
                UnityEngine.Debug.LogError("Description fetch failed: " + www.error);
                resultText.text = "Error: " + www.error;
            }
        }
    }


    IEnumerator SendImageToServer(byte[] imageData)
    {
        UnityEngine.Debug.Log("Sending image to server...");

        WWWForm form = new WWWForm();
        form.AddBinaryData("file", imageData, "capturedImage.jpg", "image/jpeg");

        using (UnityWebRequest www = UnityWebRequest.Post("http://192.168.197.97:8000/detect/", form))
        {
            yield return www.SendWebRequest();

            if (www.result == UnityWebRequest.Result.Success)
            {
                string json = www.downloadHandler.text;
                DetectionResponse response = JsonUtility.FromJson<DetectionResponse>(json);

                string displayText = "This is:\n";
                foreach (var detection in response.detections)
                {
                    displayText += $"{detection.name} ({detection.color})\n";
                }

                // Show the results in the UI
                resultText.text = displayText;
                resultTextObj.SetActive(true);
                exitButton.SetActive(true);
                readMoreButton.SetActive(true);
            }
            else
            {
                resultText.text = "Error: " + www.error;
                resultTextObj.SetActive(true);
                UnityEngine.Debug.LogError("Image upload failed: " + www.error);
            }
        }
    }


    void CaptureCameraImage()
    {
        if (cameraManager != null && cameraManager.TryAcquireLatestCpuImage(out XRCpuImage image))
        {
            UnityEngine.Debug.Log("Captured camera image!");

            // Convert to Texture2D
            XRCpuImage.ConversionParams conversionParams = new XRCpuImage.ConversionParams
            {
                inputRect = new RectInt(0, 0, image.width, image.height),
                outputDimensions = new Vector2Int(image.width, image.height),
                outputFormat = TextureFormat.RGBA32,
                transformation = XRCpuImage.Transformation.MirrorY
            };

            // Create buffer and texture
            int size = image.GetConvertedDataSize(conversionParams);
            var buffer = new NativeArray<byte>(size, Allocator.Temp);
            image.Convert(conversionParams, buffer);
            image.Dispose();

            Texture2D texture = new Texture2D(conversionParams.outputDimensions.x, conversionParams.outputDimensions.y, conversionParams.outputFormat, false);
            texture.LoadRawTextureData(buffer);
            texture.Apply();
            buffer.Dispose();

            // OPTIONAL: Display the captured image in the RawImage UI element
            if (previewImage != null)
            {
                previewImage.texture = texture;
                previewImage.gameObject.SetActive(true); // Make sure the RawImage is visible
            }

            UnityEngine.Debug.Log("Captured image displayed!");

            // Convert Texture2D to byte array (JPEG or PNG)
            byte[] imageBytes = texture.EncodeToJPG(); // You can use EncodeToPNG() if you prefer PNG

            // Send image to the Node.js server
            StartCoroutine(SendImageToServer(imageBytes));
        }
        else
        {
            UnityEngine.Debug.LogWarning("Couldn't acquire camera image.");
        }
    }

    // Update is called once per frame
    void Update() { }
}