<template>
  <div id="flash" v-if="flashMessage" role="alert">
    <FlashMessage :type="type" :message="message" />
  </div>

  <div id="app" class="mx-auto max-w-md p-6 shadow-md rounded-lg">
    <h1 class="text-2xl font-bold mb-4">Robot Control Panel</h1>

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
import FlashMessage from "./components/FlashMessage.vue";

export default {
  name: "App",
  components: {
    FlashMessage
  },
  data() {
    return {
      speed: 1,
      distance: 0,
      angle: 0,
      type: "",
      message: "",
      flashMessage: ""
    };
  },
  methods: {
    async sendInstruction() {
      axios.post("http://localhost:8000/drive/", {
          speed: this.speed,
          distance: this.distance,
          angle: -this.angle
        })
      .then(response => {
        this.flashMessage = "Instruction sent successfully";
        this.type = "success";
        this.message = this.flashMessage;
        setTimeout(() => {
          this.flashMessage = "";
        }, 5000);
      })
      .catch(error => {
        if (error.response && error.response.data && error.response.data.detail) {
          const details = error.response.data.detail;
          this.flashMessage = details.map(detail => detail.msg).join(", ");
        } else {
          this.flashMessage = "Error sending instruction: " + error.message;
        }
        this.type = "error";
        this.message = this.flashMessage;
        setTimeout(() => {
          this.flashMessage = "";
        }, 5000);
      })
    },
    connectToRobot() {
      axios.get("http://localhost:8000/connect_to_robot/")
        .then(response => {
          this.flashMessage = "Connected to the robot";
          this.type = "success";
          this.message = response.data.message;
          setTimeout(() => {
            this.flashMessage = "";
          }, 5000);
        })
        .catch(error => {
          this.flashMessage = "Error connecting to the robot: " + (error.response ? error.response.data.detail : error.message);
          this.type = "error";
          this.message = this.flashMessage;
          setTimeout(() => {
            this.flashMessage = "";
          }, 5000);
        });
    },
    stopRobot() {
      axios.post('http://localhost:8000/stop/')
        .then(response => {
          this.flashMessage = response.data.message;
          this.type = "success";
          this.message = response.data.message;
          setTimeout(() => {
            this.flashMessage = "";
          }, 5000);
        })
        .catch(error => {
          this.flashMessage = "Error stopping the robot: " + (error.response ? error.response.data.detail : error.message);
          this.type = "error";
          this.message = this.flashMessage;
          setTimeout(() => {
            this.flashMessage = "";
          }, 5000);
        });
    }
  }
};
</script>
