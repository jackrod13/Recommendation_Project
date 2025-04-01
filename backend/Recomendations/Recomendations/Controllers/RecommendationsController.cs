using Microsoft.AspNetCore.Mvc;
using System.Diagnostics;
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;

namespace RecommenderApi.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class RecommendationsController : ControllerBase
    {
        private readonly IHttpClientFactory _httpClientFactory;

        public RecommendationsController(IHttpClientFactory httpClientFactory)
        {
            _httpClientFactory = httpClientFactory;
        }

        public class RecommendRequest
        {
            public string UserID { get; set; }
        }

        public class RecommendResponse
        {
            public List<int> Collaborative { get; set; }
            public List<int> Content { get; set; }
            public List<int> Azure { get; set; }
        }

        [HttpPost]
        public async Task<IActionResult> Post([FromBody] RecommendRequest request)
        {
            
            var collaborative = RunPythonScript("collab_model.py", request.UserID);
            var content = RunPythonScript("content_model.py", request.UserID);
            var azure = await CallAzureEndpointAsync(request.UserID);

            var result = new RecommendResponse
            {
                Collaborative = collaborative,
                Content = content,
                Azure = azure
            };

            return Ok(result);
        
        }

        // Optional: Python integration (disabled for now)
        private List<int> RunPythonScript(string scriptName, string userID)
        {
            var psi = new ProcessStartInfo
            {
                FileName = "python",
                Arguments = $"{scriptName} {userID}",
                RedirectStandardOutput = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            var process = Process.Start(psi);
            var output = process.StandardOutput.ReadToEnd();
            process.WaitForExit();

            return output.Split(',').Select(int.Parse).ToList();
        }

        // Optional: Azure ML integration (disabled for now)
        private async Task<List<int>> CallAzureEndpointAsync(string userID)
        {
            var client = _httpClientFactory.CreateClient();
            var uri = "YOUR_AZURE_ENDPOINT_URL";

            client.DefaultRequestHeaders.Authorization =
                new AuthenticationHeaderValue("Bearer", "YOUR_AZURE_KEY");

            var payload = new
            {
                Inputs = new { user_id = userID }
            };

            var json = JsonSerializer.Serialize(payload);
            var content = new StringContent(json, Encoding.UTF8, "application/json");

            var response = await client.PostAsync(uri, content);
            var result = await response.Content.ReadAsStringAsync();

            return JsonSerializer.Deserialize<List<int>>(result);
        }
    }
}
