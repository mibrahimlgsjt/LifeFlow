document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('donorForm');
    const donorList = document.getElementById('donorList');
    
    // Load donors on page load
    fetchDonors();
    
    // Handle form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(form);
        const donorData = Object.fromEntries(formData.entries());
        
        try {
            const response = await fetch('/api/donors', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(donorData)
            });
            
            if (response.ok) {
                alert('Donor added successfully!');
                form.reset();
                fetchDonors();
            } else {
                const error = await response.json();
                alert(`Error: ${error.error}`);
            }
        } catch (error) {
            alert(`Network error: ${error}`);
        }
    });
    
    // Fetch and display donors
    async function fetchDonors() {
        try {
            const response = await fetch('/api/donors');
            const donors = await response.json();
            
            donorList.innerHTML = donors.map(donor => `
                <div class="donor">
                    <h3>${donor.name}</h3>
                    <p>Blood Type: ${donor.blood_type}</p>
                    <p>Email: ${donor.email}</p>
                    <p>Phone: ${donor.phone}</p>
                </div>
            `).join('');
        } catch (error) {
            console.error('Error fetching donors:', error);
        }
    }
});