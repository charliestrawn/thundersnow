const fakeAuth = {
    isAuthenticated: false,
    authenticate(user, pass, cb) {
      console.log(user);
      console.log(pass);
      this.isAuthenticated = true
      setTimeout(cb, 100)
    },
    signout(cb) {
      this.isAuthenticated = false
      setTimeout(cb, 100)
    }
};

export default fakeAuth;
