

// Fetch statistics on page load
window.addEventListener('DOMContentLoaded', () => {
    sliderValue.textContent = slider.value;
    const initialMaxLimit = slider.value || initialMaxLimit;  // Use the slider value on page load, default to 100
    fetchStats(0, initialMaxLimit);
    fetchStats(1, initialMaxLimit);
    fetchStats(2, initialMaxLimit);
});


// Update the value display when the slider changes
slider.addEventListener('input', function () {
    sliderValue.textContent = slider.value;
});

// Fetch new data when the slider stops being dragged
slider.addEventListener('change', function () {
    const maxLimit = slider.value;
    fetch(`/data.html?max_limit=${maxLimit}`, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
        .then(response => response.json())
        .then(data => {
            // Assuming the server returns the new labels and data arrays
            chart1.data.labels = data.labels;
            chart1.data.datasets[0].data = data.data1_1;
            chart1.data.datasets[1].data = data.data1_2;
            chart1.data.datasets[2].data = data.data1_3;
            chart1.update();

            chart2.data.labels = data.labels;
            chart2.data.datasets[0].data = data.data2_1;
            chart2.data.datasets[1].data = data.data2_2;
            chart2.data.datasets[2].data = data.data2_3;
            chart2.update();
        })
        .catch(err => console.error('Error fetching data:', err));


    // Fetch and update statistics
    fetchStats(2, maxLimit);
    fetchStats(1, maxLimit);
    fetchStats(0, maxLimit);
});



function formatDateISO(d) {
    return d.toISOString().split('T')[0];
}

function setSelectedDay(d) {
    selectedDay = d;
    dayPicker.value = formatDateISO(d);
    dayLabel.textContent = formatDateISO(d);
    fetchDayData();
}

// Statistics information
function fetchStats(sensorId, maxLimit) {
	fetch(`/stats?sensor_id=${sensorId}&max_limit=${maxLimit}`)
        .then(response => response.json())
        .then(stats => {
		    document.getElementById(`stat-high-${sensorId}`).textContent = stats.high ?? 'N/A';
		    document.getElementById(`stat-low-${sensorId}`).textContent = stats.low ?? 'N/A';
		    document.getElementById(`stat-mean-${sensorId}`).textContent = stats.mean ?? 'N/A';
		    document.getElementById(`stat-time-early`).textContent = stats.earliest_time ?? 'N/A';
		    document.getElementById(`stat-time-late`).textContent = stats.latest_time ?? 'N/A';
        })
        .catch(error => console.error('Error fetching stats:', error));
}



