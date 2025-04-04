using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;

namespace RecommenderApi.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class RecommendationsController : ControllerBase
    {
        public class RecommendRequest
        {
            public string UserID { get; set; }
        }

        public class RecommendResponse
        {
            public List<long> Collaborative { get; set; }
            public List<long> Content { get; set; }
            public List<long> Azure { get; set; }
        }

        [HttpPost]
        public IActionResult Post([FromBody] RecommendRequest request)
        {
            try
            {
                Console.WriteLine($"🔍 Dummy request received for user: {request.UserID}");

                var result = new RecommendResponse
                {
                    Collaborative = new List<long> { 101, 102, 103, 104 },
                    Content = new List<long> { 201, 202, 203, 204 },
                    Azure = new List<long> { 301, 302, 303, 304 }
                };

                return Ok(result);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Exception: {ex.Message}");
                return StatusCode(500, $"Internal server error: {ex.Message}");
            }
        }
    }
}
