const sdk = require("microsoft-cognitiveservices-speech-sdk");
const fs = require("fs");

// ⚠️ Reemplaza con tus datos de Azure
const AZURE_KEY = "TU_CLAVE_AZURE";
const AZURE_REGION = "southcentralus"; // o la que uses

const archivo = "audio_para_transcribir.wav";

const transcribir = () => {
  const pushStream = sdk.AudioInputStream.createPushStream();
  fs.createReadStream(archivo).on("data", function(arrayBuffer) {
    pushStream.write(arrayBuffer.buffer);
  }).on("end", function() {
    pushStream.close();
  });

  const audioConfig = sdk.AudioConfig.fromStreamInput(pushStream);
  const speechConfig = sdk.SpeechConfig.fromSubscription(AZURE_KEY, AZURE_REGION);
  speechConfig.speechRecognitionLanguage = "es-CL";

  const recognizer = new sdk.SpeechRecognizer(speechConfig, audioConfig);

  recognizer.recognizeOnceAsync(result => {
    console.log("\n📄 TRANSCRIPCIÓN:");
    console.log(result.text);
    recognizer.close();
  });
};

transcribir();



