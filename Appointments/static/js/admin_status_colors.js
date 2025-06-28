document.addEventListener('DOMContentLoaded', function () {
    const selects = document.querySelectorAll('td.field-status select');

    selects.forEach(select => {
        function updateColor() {
            const value = select.value;
            let color = '#6c757d'; // default gray

            if (value === 'confirmed') color = '#28a745';
            else if (value === 'pending') color = '#FFA500';
            else if (value === 'cancelled') color = '#dc3545';
            else if (value === 'to-be-rescheduled') color = '#007bff';
            
            select.style.backgroundColor = color;
        }

        // Initial color set
        updateColor();

        // Update on change
        select.addEventListener('change', updateColor);
    });
});
