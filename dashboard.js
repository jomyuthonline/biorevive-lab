document.addEventListener('DOMContentLoaded', () => {
    // Current time for the log
    const now = new Date();
    const timeString = `${now.getHours()}:${now.getMinutes().toString().padStart(2, '0')}`;

    // You can add logic here to fetch real data from an API if needed
    console.log("BioRevive Command Center Initialized at " + timeString);

    // Dynamic Greeting based on time
    const brand = document.querySelector('.brand');
    const hour = now.getHours();
    let greeting = 'BIOREVIVE';
    
    if (hour < 12) greeting = 'GOOD MORNING, BIOREVIVE';
    else if (hour < 18) greeting = 'GOOD AFTERNOON, BIOREVIVE';
    else greeting = 'GOOD EVENING, BIOREVIVE';
    
    // Optional: Update greeting
    // brand.innerText = greeting;
});
