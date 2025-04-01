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
            try
            {
                var collaborative = RunPythonScript("load_collab_model.py", request.UserID);
                var content = RunPythonScript("content_model.py", request.UserID);
                var azure = new List<int> { 999, 998, 997, 996, 995 }; // Placeholder for Azure ML

                var result = new RecommendResponse
                {
                    Collaborative = collaborative,
                    Content = content,
                    Azure = azure
                };

                return Ok(result);
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Internal server error: {ex.Message}");
            }
        }

        private List<int> RunPythonScript(string scriptName, string userID)
        {
            var psi = new ProcessStartInfo
            {
                FileName = "python",
                Arguments = $"{scriptName} {userID}",
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true,
                WorkingDirectory = AppDomain.CurrentDomain.BaseDirectory
            };

            var process = new Process { StartInfo = psi };

            process.Start();

            string output = process.StandardOutput.ReadToEnd();
            string error = process.StandardError.ReadToEnd();

            process.WaitForExit();

            if (!string.IsNullOrEmpty(error))
            {
                throw new Exception($"Python error: {error}");
            }

            return output.Split(',').Select(id => int.Parse(id.Trim())).ToList();
        }

        // Optional Azure ML logic (not yet active)
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
