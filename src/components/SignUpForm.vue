<template>
    <div class="form-overlay">
      <div class="form-container">
        <div class="form-logo">
          <img alt="F1 Logo" src="@/assets/f1-logo.png" />
        </div>
  
        <h2>Sign Up</h2>
        <form @submit.prevent="handleSignUp">
          <div class="form-group">
            <label for="email">Email</label>
            <input
              type="email"
              id="email"
              v-model="email"
              placeholder="Enter your email"
              required
            />
          </div>
  
          <div class="form-group">
            <label for="password">Password</label>
            <input
              type="password"
              id="password"
              v-model="password"
              placeholder="Enter your password"
              required
            />
          </div>
  
          <div class="form-group terms">
            <input
              type="checkbox"
              id="terms"
              v-model="terms"
            />
            <label for="terms">I agree to the terms and conditions</label>
          </div>
  
          <div class="form-actions">
            <button type="submit" class="btn-primary" :disabled="!terms">
              Sign Up
            </button>
            <button type="button" class="btn-secondary" @click="$emit('close')">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
</template>
  
<script>
  export default {
    data() {
      return {
        email: "",
        password: "",
        terms: false,
        logged: true
      };
    },
    methods: {
      handleSignUp() {
        if (this.email && this.password && this.terms) {
          alert(`Signed up successfully with email: ${this.email}`);
          this.$emit("close", this.logged); 
        } else {
          alert("Please complete all fields and agree to the terms.");
        }
      },
    },
  };
</script>
  
  <style>
  .form-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.7); 
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999; 
  }
  
  .form-container {
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2); 
    width: 350px;
    padding: 20px;
    text-align: center;
    position: relative;
  }
  
  .form-logo img {
    width: 80px;
    margin-bottom: 15px;
  }
  
  h2 {
    margin-bottom: 20px;
    color: #2c3e50; 
    font-weight: bold;
  }
  
  .form-group {
    margin-bottom: 15px;
    text-align: left;
  }
  
  label {
    display: block;
    font-size: 14px;
    margin-bottom: 5px;
    color: #2c3e50;
  }
  
  input[type="email"],
  input[type="password"] {
    width: 100%;
    padding: 10px;
    font-size: 14px;
    border: 1px solid #ddd;
    border-radius: 5px;
    outline: none;
    transition: all 0.3s ease;
  }
  
  input[type="email"]:focus,
  input[type="password"]:focus {
    border-color: #b94242; 
  }
  
  .terms {
    display: flex;
    align-items: center;
  }
  
  .terms input[type="checkbox"] {
    margin-right: 10px;
  }
  
  .form-actions {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
  }
  
  button {
    padding: 10px 20px;
    font-size: 14px;
    border-radius: 5px;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .btn-primary {
    background-color: #ff0000; 
    color: white;
    font-weight: bold;
  }
  
  .btn-primary:hover {
    background-color: #cc0000;
  }
  
  .btn-primary:disabled {
    background-color: #ddd; 
    cursor: not-allowed;
  }
  
  .btn-secondary {
    background-color: #ddd;
    color: #2c3e50;
  }
  
  .btn-secondary:hover {
    background-color: #bbb;
  }
  </style>
  