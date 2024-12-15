<template>
 <div class="navbar">

  <div class="logo">
    <img alt="F1 Logo" src="@/assets/f1-logo.png"/>
  </div>

  <div class="navbar-header">
    <nav>
      <router-link class="nav-button" to="/">Home</router-link>
      <router-link class="nav-button" to="/about">About</router-link>
    </nav>

      <button class =sign-button v-if="isSigned" @click="logOut">Log Out</button>
      <button class =sign-button v-else @click="signIn">Sign in</button>

      
  </div>

 </div> 
  <div v-if="showSign">
    <SignUpForm @close="signIn"/>
  </div>
  <router-view/>

  <div class="footer">
    <p class="footer-text">Copyright @ AfterForeverPi 2024</p>

  </div>
  
</template>

<script>
  import SignUpForm from "./components/SignUpForm.vue";

  export default {
    name: 'App',
    components : {SignUpForm},
    data(){
      return {
        isSigned: false,
        showSign: false
      }
    },
    methods: {
      signIn(logged){
        this.showSign = !this.showSign;
        this.isSigned = logged;
      },
      logOut(){
        this.isSigned = false;
      }
      
    }
  }

</script>



<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

*{
 
 font-family: Avenir, Helvetica, Arial, sans-serif; 
 padding: 0;
 margin: 0;

 box-sizing: border-box;
 
}

.logo img{
  height: 40px;
  width: auto;
}

.navbar{
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 5px 30px;
  background-color: #222121;

}

.navbar-header{
  padding: 0px 40px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.nav-button {
  display: inline-block;
  padding: 10px 20px; /* Adjust padding for better size */
  font-size: 16px; /* Make text size consistent */
  font-weight: bold;
  color: white; /* Default text color */
  text-decoration: none; /* Remove underline */
  border: 2px solid white; /* White border */
  border-radius: 5px; /* Rounded corners */
  transition: all 0.3s ease; /* Smooth transition effect */
  margin-left: 10px; /* Spacing between buttons */
}

/* Hover effect: White to red */
.nav-button:hover {
  color: #fff;
  background-color: #ff0000; /* Red background on hover */
  border-color: #ff0000; /* Red border on hover */
}

.sign-button {

  display: inline-block;
  padding: 10px 20px; /* Padding for button size */
  font-size: 16px; /* Font size for better readability */
  font-weight: bold; /* Bold text */
  color: white; /* White text color */
  text-decoration: none; /* Remove underline */
  background-color: #ff0000; /* Red background by default */
  border: 2px solid #ff0000; /* Red border by default */
  border-radius: 5px; /* Rounded corners */
  transition: all 0.3s ease; /* Smooth transition for hover effects */
  margin-left: 10px; /* Space between buttons */
  cursor: pointer; /* Pointer cursor for buttons */
}

.sign-button:hover {
  background-color: #cc0000; /* Slightly darker red on hover */
  border-color: #cc0000; /* Darker red border on hover */
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #fff;
  background-color: #ff0000; /* Red background on hover */
  border-color: #ff0000;
}

.footer{

position: fixed;
left: 0;
bottom: 0;
width: 100%;
display: flex;
justify-content: center;
align-items: center;

padding: 30px;

color: #F9FAF8;
background-color: #222121;



}
</style>
