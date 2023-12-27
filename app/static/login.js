function validateLogin(event) {
    // Get input values
    var form = document.querySelector('.login-form');
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
  
    // Simple validation (you may want to implement more robust validation)
    if (!username || !password) {
      alert('Please enter both username and password.');
      return;
    }
}