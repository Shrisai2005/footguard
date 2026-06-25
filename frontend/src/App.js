import React, { useState } from "react";
import {
  Container,
  Typography,
  Button,
  Card,
  CardContent,
  Grid,
  Divider,
  Box,
  CircularProgress,
} from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import HealthAndSafetyIcon from "@mui/icons-material/HealthAndSafety";

function App() {
  const [result, setResult] = useState(null);
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);

  const uploadImage = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setImage(URL.createObjectURL(file));
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:8000/predict-image", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setResult(data);
    } catch (error) {
      console.error(error);
      alert("Backend connection failed. Make sure FastAPI is running.");
    }

    setLoading(false);
  };

  const getSeverityColor = (severity) => {
    if (severity === "Severe") return "#d32f2f";
    if (severity === "Moderate") return "#ed6c02";
    return "#2e7d32";
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        background: "linear-gradient(135deg, #0f172a 0%, #1e293b 35%, #0ea5e9 100%)",
        py: 5,
      }}
    >
      <Container maxWidth="lg">
        {/* Header */}
        <Card
          sx={{
            borderRadius: 4,
            boxShadow: 4,
            mb: 4,
            p: 2,
            background: "rgba(255,255,255,0.95)",
          }}
        >
          <CardContent>
            <Box display="flex" alignItems="center" gap={2}>
              <HealthAndSafetyIcon sx={{ fontSize: 42, color: "#1976d2" }} />
              <Box>
                <Typography variant="h4" fontWeight="bold" sx={{ color: "#0f172a" }}>
                  FootGuard AI Dashboard
                </Typography>
                <Typography variant="body1" sx={{ color: "#475569" }}>
                  Intelligent Diabetic Foot Ulcer Detection & Medical Analysis
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>

        {/* Upload Section */}
        <Card
          sx={{
            borderRadius: 5,
            boxShadow: "0 10px 30px rgba(0,0,0,0.15)",
            mb: 4,
            textAlign: "center",
            p: 3,
            background: "rgba(255,255,255,0.96)",
            backdropFilter: "blur(10px)",
          }}
        >
          <Typography variant="h6" gutterBottom>
            Upload Patient Foot Image
          </Typography>

          <Button
            variant="contained"
            sx={{
              background: "linear-gradient(90deg, #2563eb, #06b6d4)",
              boxShadow: "0 8px 20px rgba(37,99,235,0.35)",
              '&:hover': {
                background: "linear-gradient(90deg, #1d4ed8, #0891b2)",
              }
            }}
            component="label"
            size="large"
            startIcon={<CloudUploadIcon />}
            sx={{
              borderRadius: 3,
              px: 4,
              py: 1.2,
              textTransform: "none",
              fontWeight: "bold",
            }}
          >
            Upload Image
            <input
              hidden
              type="file"
              accept="image/*"
              onChange={uploadImage}
            />
          </Button>
        </Card>

        {/* Image Preview */}
        {image && (
          <Card
            sx={{
              borderRadius: 4,
              boxShadow: 3,
              mb: 4,
              textAlign: "center",
              p: 3,
            }}
          >
            <Typography variant="h6" gutterBottom>
              Image Preview
            </Typography>

            <img
              src={image}
              alt="preview"
              style={{
                width: 280,
                borderRadius: 16,
                boxShadow: "0 8px 24px rgba(0,0,0,0.12)",
              }}
            />
          </Card>
        )}

        {/* Loading */}
        {loading && (
          <Box textAlign="center" my={4}>
            <CircularProgress />
            <Typography mt={2}>Analyzing image with AI...</Typography>
          </Box>
        )}

        {/* Result Section */}
        {result && !loading && (
          <Grid container spacing={3}>
            {/* Prediction Card */}
            <Grid item xs={12} md={4}>
              <Card sx={{ borderRadius: 5, boxShadow: "0 12px 30px rgba(0,0,0,0.15)", height: "100%", background: "rgba(255,255,255,0.97)" }}>
                <CardContent>
                  <Typography variant="h6" fontWeight="bold">
                    Prediction Report
                  </Typography>

                  <Divider sx={{ my: 2 }} />

                  <Typography mb={1}>
                    <b>Ulcer Detected:</b> {result.ulcer_detected ? "Yes" : "No"}
                  </Typography>

                  <Typography mb={1}>
                    <b>Stage:</b> {result.stage}
                  </Typography>

                  <Typography
                    mb={1}
                    sx={{
                      color: getSeverityColor(result.severity),
                      fontWeight: "bold",
                    }}
                  >
                    <b>Severity:</b> {result.severity}
                  </Typography>

                  <Typography>
                    <b>Confidence:</b> {result.confidence?.toFixed(3)}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            {/* Medical Insights */}
            <Grid item xs={12} md={8}>
              <Card sx={{ borderRadius: 5, boxShadow: "0 12px 30px rgba(0,0,0,0.15)", background: "rgba(255,255,255,0.97)" }}>
                <CardContent>
                  <Typography variant="h6" fontWeight="bold">
                    Medical Insights
                  </Typography>

                  <Divider sx={{ my: 2 }} />

                  <Typography
                    sx={{
                      whiteSpace: "pre-line",
                      lineHeight: 1.9,
                      color: "#333",
                    }}
                  >
                    {result.ai_explanation || "Medical explanation unavailable."}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        )}
      </Container>
    </Box>
  );
}

export default App;
