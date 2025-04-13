using System.Collections;
using Unity.Collections;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.XR.ARFoundation;
using UnityEngine.XR.ARSubsystems;
using UnityEngine.Networking;


public class UI : MonoBehaviour
{
    public GameObject startButton; // Just a start button that will hide the greetings canvas
    public GameObject captureButton;
    public GameObject[] greetingCanvas; // All the game objects from the greeting canvas that need to be hidden later
    public GameObject avatar; // Access the avatar
    public RectTransform avatarTransform; // Used to make the avatar smaller
    public Vector2 bottomLeftAnchorPos;

    // Selecting area of interest
    public ARCameraManager cameraManager;
    public RawImage previewImage;
    public GameObject previewImageObj;

    // Start is called before the first frame update
    void Start()
    {
        captureButton.SetActive(false);
        previewImageObj.SetActive(false);
        startButton.GetComponent<Button>().onClick.AddListener(OnStartClicked);

        // Add listener to the button click
        if (captureButton != null)
        {
            captureButton.GetComponent<Button>().onClick.AddListener(OnCaptureButtonClicked);
        }
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

    // Function to handle button click
    void OnCaptureButtonClicked()
    {
        UnityEngine.Debug.Log("Button clicked!");

        // Capture the image from the AR camera
        CaptureCameraImage();
        previewImageObj.SetActive(true);
    }

    IEnumerator SendImageToServer(byte[] imageData)
    {
        UnityEngine.Debug.Log("Sending image to server...");

        WWWForm form = new WWWForm();
        form.AddBinaryData("file", imageData, "capturedImage.jpg", "image/jpeg");

        using (UnityWebRequest www = UnityWebRequest.Post("http://192.168.199.97:8000/detect", form))
        {
            yield return www.SendWebRequest();

            if (www.result == UnityWebRequest.Result.Success)
            {
                UnityEngine.Debug.Log("Image successfully uploaded!");
            }
            else
            {
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
    void Update(){}
}
