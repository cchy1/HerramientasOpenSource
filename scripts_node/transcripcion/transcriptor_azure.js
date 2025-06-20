require('dotenv').config();
const sdk = require("microsoft-cognitiveservices-speech-sdk");
const fs = require("fs");
const path = require("path");

// Obtener archivo de audio desde argumentos o usar el predeterminado
const inputFile = process.argv[2] || "audio_reconvertido.wav";

// Generar nombre del archivo de salida automáticamente
const baseName = path.basename(inputFile, path.extname(inputFile));
const outputFile = `${baseName}_transcripcion.txt`;

// Configuración de Azure
const AZURE_KEY = process.env.AZURE_SPEECH_KEY;
const AZURE_REGION = process.env.AZURE_SPEECH_REGION;
const speechConfig = sdk.SpeechConfig.fromSubscription(AZURE_KEY, AZURE_REGION);
speechConfig.speechRecognitionLanguage = "es-CL";

// Crear stream de entrada para el audio
const pushStream = sdk.AudioInputStream.createPushStream();
fs.createReadStream(inputFile)
  .on("data", arrayBuffer => pushStream.write(arrayBuffer))
  .on("end", () => pushStream.close());

// Configurar el reconocimiento
const audioConfig = sdk.AudioConfig.fromStreamInput(pushStream);
const recognizer = new sdk.SpeechRecognizer(speechConfig, audioConfig);

// Ejecutar reconocimiento
recognizer.recognizeOnceAsync(result => {
  console.log("\n🧠 TRANSCRIPCIÓN:");
  console.log(result.text);

  fs.writeFileSync(outputFile, result.text, "utf8");
  console.log(`\n📝 Archivo guardado: ${outputFile}`);

  recognizer.close();
});
