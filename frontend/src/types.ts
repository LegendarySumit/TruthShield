export interface PredictionResult {
  prediction: string;
  confidence: number;
  explanation: string;
  model_version?: string;
}
