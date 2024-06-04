<template>

    <div id="flash" v-if="flashMessage" role="alert">
      <FlashMessage :type=type :message=message />
    </div>

  <div id="app" class="mx-auto max-w-md p-6 shadow-md rounded-lg">
    <h1 class="text-2xl font-bold mb-4">Robot Control Panel</h1>
    <!-- Flashbericht weergeven -->

    <div class="mb-4">
      <button class="bg-nvwa-grijs-2" @click="connectToRobot">Connect to Robot</button>
    </div>
    <div class="mb-4">
      <label for="speed" class="block mb-1">Speed (m/s):</label>
      <input v-model.number="speed" type="number" id="speed" min="-2" max="2" step="1" class="w-full p-2 border border-gray-300 rounded-md" />
    </div>
    <div class="mb-4">
      <label for="distance" class="block mb-1">Distance (m):</label>
      <input v-model.number="distance" type="number" id="distance" min="0" max="100" class="w-full p-2 border border-gray-300 rounded-md" />
    </div>
    <div class="mb-4">
      <label for="angle" class="block mb-1">Steering Angle (radians):</label>
      <div class="flex items-center justify-center mb-2">
        <span class="pr-2">Left</span>
        <input v-model.number="angle" type="range" id="angle" min="-1.5" max="0.8" step="0.01" class="w-4/5 p-2 border border-gray-300 rounded-md" />
        <span class="pl-2">Right</span>
      </div>
      <div class="flex justify-center">
        <span>{{ -angle }}</span>
      </div>
    </div>
    <button @click="sendInstruction" class="w-full py-2 px-4 bg-donker-blue text-white rounded-md hover:bg-hemel-blue">Send Instruction</button><br />
    <button @click="stopRobot" class="w-full py-2 mt-2 px-4 bg-nvwa-rood text-white rounded-md hover:bg-hemel-blue">Stop Robot</button>
  </div>
</template>

<script>
import axios from "axios";
import UploadPath from "./components/UploadPath.vue"; 
import FlashMessage from "./components/FlashMessage.vue";


export default {
  name: "App",
  components: {
    UploadPath
  },
  data() {
    return {
      speed: 1,
      distance: 0,
      angle: 0,
      type: "",
      message: "",
      flashMessage: "",
    };
  },
  methods: {
    async sendInstruction() {
      try {
        await axios.post("http://localhost:8000/drive/", {
          speed: this.speed,
          distance: this.distance,
          angle: -this.angle     
        });
        console.log("Instruction sent successfully");
        this.flashMessage = "Instruction sent successfully";
        this.type = "success";
        this.message = this.flashMessage

        setTimeout(() => {
            this.flashMessage = "";
          }, 5000);
      } catch (error) {
        this.flashMessage = "Error sending instruction: " + error.message;
        this.type = "error"
        this.message = this.flashMessage
        console.error("Error sending instruction:", error);
        
        setTimeout(() => {
          this.flashMessage = "";
        }, 5000);
      }
    },
    connectToRobot() {
      // Doe een HTTP GET-verzoek naar de connect_to_robot endpoint
      axios.get("http://localhost:8000/connect_to_robot/")
        .then(response => {
          console.log("Connected to the robot:", response.data);
          // Zet de flashMessage
          this.flashMessage = "Connected to the robot";
          this.type = "success"
          this.message = "Established connection to Capra Hircus"
          // Wis de flashMessage na 5 seconden
          setTimeout(() => {
            this.flashMessage = "";
          }, 5000);
        })
        .catch(error => {
          // Zet de flashMessage in errorMessage
          this.flashMessage = "Error connecting to the robot: " + error;
          this.type = "error"
          this.message = this.flashMessage
          console.error("Error connecting to the robot:", error);
          // Wis de flashMessage na 5 seconden
          setTimeout(() => {
            this.flashMessage = "";
          }, 5000);
        });
    },
    stopRobot() {
      axios.post('http://localhost:8000/stop/')
      .then(response => {
        console.log(response.data.message)
          this.flashMessage = response;
          this.type = "success"
          this.message = response.data.message
          // Wis de flashMessage na 5 seconden
          setTimeout(() => {
            this.flashMessage = "";
          }, 5000);
      })
    }
  }
};
</script>

<style>
/* Voeg eventuele stijlen toe */
</style>
