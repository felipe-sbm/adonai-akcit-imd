using Microsoft.AspNetCore.Components.Forms;
using System.Net.Http.Json;
using System.Text.Json;

namespace adonai.Services
{
    public record CodeReviewResult(bool Success, string Message, string? Emotion = null);

    public class CodeReviewService
    {
        private readonly HttpClient _httpClient;
        public CodeReviewService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<CodeReviewResult> SubmitCodeReviewAsync(
            IBrowserFile? file,
            string task)
        {
            HttpContent content;

            if (file is null)
            {
                content = JsonContent.Create(new { task = task ?? string.Empty });
            }
            else
            {
                var multipartContent = new MultipartFormDataContent();

                var stream = file.OpenReadStream(maxAllowedSize: 1024 * 1024 * 50);
                var streamContent = new StreamContent(stream);
                streamContent.Headers.ContentType = new System.Net.Http.Headers.MediaTypeHeaderValue(
                    file.ContentType ?? "application/octet-stream");

                multipartContent.Add(streamContent, "file", file.Name);
                multipartContent.Add(new StringContent(task ?? ""), "task");
                content = multipartContent;
            }

            using var response = await _httpClient.PostAsync("/api/v1/review", content);
            var body = await response.Content.ReadAsStringAsync();

            if (response.IsSuccessStatusCode)
            {
                return ParseSuccess(body);
            }

            return ParseError(body, (int)response.StatusCode);
        }

        private static CodeReviewResult ParseSuccess(string json)
        {
            try
            {
                using var doc = JsonDocument.Parse(json);
                var root = doc.RootElement;

                var review = GetString(root, "review");
                var aiResponse = GetString(root, "ai_response");
                var emotion = GetString(root, "emotion");

                var message = !string.IsNullOrWhiteSpace(review)
                    ? review
                    : !string.IsNullOrWhiteSpace(aiResponse)
                        ? aiResponse
                        : "Análise concluída com sucesso.";

                return new CodeReviewResult(true, message!, emotion);
            }
            catch
            {
                return new CodeReviewResult(true, "Análise concluída, mas não foi possível interpretar a resposta.");
            }
        }

        private static CodeReviewResult ParseError(string json, int statusCode)
        {
            try
            {
                using var doc = JsonDocument.Parse(json);
                var root = doc.RootElement;

                var error = GetString(root, "error");
                if (!string.IsNullOrWhiteSpace(error))
                {
                    return new CodeReviewResult(false, error!);
                }

                if (root.TryGetProperty("errors", out var errorsElement) &&
                    errorsElement.ValueKind == JsonValueKind.Array)
                {
                    var errors = errorsElement
                        .EnumerateArray()
                        .Select(x => x.GetString())
                        .Where(x => !string.IsNullOrWhiteSpace(x));

                    var combined = string.Join(" | ", errors!);
                    if (!string.IsNullOrWhiteSpace(combined))
                    {
                        return new CodeReviewResult(false, combined);
                    }
                }
            }
            catch
            {
            }

            return new CodeReviewResult(false, $"Erro ao enviar para análise (HTTP {statusCode}).");
        }

        private static string? GetString(JsonElement root, string propertyName)
        {
            if (root.TryGetProperty(propertyName, out var element) && element.ValueKind == JsonValueKind.String)
            {
                return element.GetString();
            }

            return null;
        }
    }
}
