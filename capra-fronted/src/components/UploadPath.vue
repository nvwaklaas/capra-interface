  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        file: null,
        uploadStatus: ""
      };
    },
    methods: {
      handleFileUpload(event) {
        this.file = event.target.files[0];
      },
      async uploadFile() {
        if (!this.file) {
          this.uploadStatus = "Select a JSON file first";
          return;
        }
  
        try {
          const formData = new FormData();
          formData.append("file", this.file);
  
          const response = await axios.post("http://localhost:8000/upload-json", formData, {
            headers: {
              "Content-Type": "multipart/form-data"
            }
          });
  
          this.uploadStatus = response.data.message;
        } catch (error) {
          this.uploadStatus = "Error uploading file";
          console.error("Error uploading file:", error);
        }
      }
    }
  };
  </script>

<template>
    <div>
      <input type="file" @change="handleFileUpload" accept=".json" />
      <button @click="uploadFile">Upload JSON File</button>
      <div v-if="uploadStatus">
        <p>{{ uploadStatus }}</p>
      </div>
    </div>
  </template>

  
  <style>
  /* Voeg eventuele stijlen toe */
  </style>
  