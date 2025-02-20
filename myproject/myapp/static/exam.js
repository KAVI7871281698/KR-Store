function toggleMenu() {
    const navLinks = document.querySelector('.nav-links');
    navLinks.classList.toggle('active'); // Toggles the visibility of the nav links
  }
  
  function toggleSearch() {
    const searchBar = document.querySelector('.search-bar');
    searchBar.style.display = searchBar.style.display === 'block' ? 'none' : 'block';
  }
  
  function searchAction() {
    const query = document.querySelector('.search-bar input').value;
    alert(`Searching for: ${query}`);
    // Implement your search functionality here
  }
  