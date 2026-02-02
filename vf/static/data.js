
// Temperature scale preference (default to Fahrenheit)
let temperatureScale = 'f';

// Fetch statistics on page load
window.addEventListener('DOMContentLoaded', () => {
    sliderValue.textContent = slider.value;
    const initialMaxLimit = slider.value || 5000;  // Use the slider value on page load, default to 5000
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
    fetch(`/data.html?max_limit=${maxLimit}&scale=${temperatureScale}`, {
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

function fetchDayData() {
    const dateStr = formatDateISO(selectedDay);

    // Fetch chart data for the selected day
    fetch(`/data.html?start_date=${dateStr}&end_date=${dateStr}&scale=${temperatureScale}`, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
        .then(response => response.json())
        .then(data => {
            // Update chart 1 (temperature)
            chart1.data.labels = data.labels;
            chart1.data.datasets[0].data = data.data1_1;
            chart1.data.datasets[1].data = data.data1_2;
            chart1.data.datasets[2].data = data.data1_3;
            chart1.update();

            // Update chart 2 (humidity)
            chart2.data.labels = data.labels;
            chart2.data.datasets[0].data = data.data2_1;
            chart2.data.datasets[1].data = data.data2_2;
            chart2.data.datasets[2].data = data.data2_3;
            chart2.update();
        })
        .catch(err => console.error('Error fetching day data:', err));

    // Fetch and update statistics for the selected day
    fetchStatsByDate(0, dateStr, dateStr);
    fetchStatsByDate(1, dateStr, dateStr);
    fetchStatsByDate(2, dateStr, dateStr);
}

function fetchStatsByDate(sensorId, startDate, endDate) {
    fetch(`/stats?sensor_id=${sensorId}&start_date=${startDate}&end_date=${endDate}&scale=${temperatureScale}`)
        .then(response => response.json())
        .then(stats => {
            // Temperature stats
            document.getElementById(`stat-temp-high-${sensorId}`).textContent = stats.temp_high ?? 'N/A';
            document.getElementById(`stat-temp-low-${sensorId}`).textContent = stats.temp_low ?? 'N/A';
            document.getElementById(`stat-temp-mean-${sensorId}`).textContent = stats.temp_mean ?? 'N/A';
            document.getElementById(`stat-temp-stddev-${sensorId}`).textContent = stats.temp_stddev ?? 'N/A';

            // Humidity stats
            document.getElementById(`stat-hum-high-${sensorId}`).textContent = stats.hum_high ?? 'N/A';
            document.getElementById(`stat-hum-low-${sensorId}`).textContent = stats.hum_low ?? 'N/A';
            document.getElementById(`stat-hum-mean-${sensorId}`).textContent = stats.hum_mean ?? 'N/A';
            document.getElementById(`stat-hum-stddev-${sensorId}`).textContent = stats.hum_stddev ?? 'N/A';

            // General stats (only update once, not per sensor)
            document.getElementById(`stat-count`).textContent = stats.count ?? 'N/A';
            document.getElementById(`stat-time-early`).textContent = stats.earliest_time ?? 'N/A';
            document.getElementById(`stat-time-late`).textContent = stats.latest_time ?? 'N/A';
        })
        .catch(error => console.error('Error fetching stats by date:', error));
}

// Initialize date picker to show today's date (but don't fetch data yet)
window.addEventListener('DOMContentLoaded', () => {
    dayPicker.value = formatDateISO(selectedDay);
    dayLabel.textContent = formatDateISO(selectedDay);
});

// Event listener for date picker input
dayPicker.addEventListener('change', function() {
    const newDate = new Date(this.value);
    if (!isNaN(newDate.getTime())) {
        setSelectedDay(newDate);
    }
});

// Event listener for previous day button
dayPrev.addEventListener('click', function() {
    const newDate = new Date(selectedDay);
    newDate.setDate(newDate.getDate() - 1);
    setSelectedDay(newDate);
});

// Event listener for next day button
dayNext.addEventListener('click', function() {
    const newDate = new Date(selectedDay);
    newDate.setDate(newDate.getDate() + 1);
    setSelectedDay(newDate);
});

// Sensor visibility controls
document.getElementById('sensor-0').addEventListener('change', function() {
    const isVisible = this.checked;
    chart1.setDatasetVisibility(0, isVisible);
    chart2.setDatasetVisibility(0, isVisible);
    chart1.update();
    chart2.update();
});

document.getElementById('sensor-1').addEventListener('change', function() {
    const isVisible = this.checked;
    chart1.setDatasetVisibility(1, isVisible);
    chart2.setDatasetVisibility(1, isVisible);
    chart1.update();
    chart2.update();
});

document.getElementById('sensor-2').addEventListener('change', function() {
    const isVisible = this.checked;
    chart1.setDatasetVisibility(2, isVisible);
    chart2.setDatasetVisibility(2, isVisible);
    chart1.update();
    chart2.update();
});

// Temperature scale toggle
document.querySelectorAll('input[name="temp-scale"]').forEach(radio => {
    radio.addEventListener('change', function() {
        temperatureScale = this.value;

        // Refetch data with new scale
        // Check if we're in date mode or slider mode
        if (dayPicker.value) {
            // If a date is selected, refresh day data
            const dateStr = formatDateISO(selectedDay);
            fetch(`/data.html?start_date=${dateStr}&end_date=${dateStr}&scale=${temperatureScale}`, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
                .then(response => response.json())
                .then(data => {
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

            fetchStatsByDate(0, dateStr, dateStr);
            fetchStatsByDate(1, dateStr, dateStr);
            fetchStatsByDate(2, dateStr, dateStr);
        } else {
            // Otherwise, use slider value
            const maxLimit = slider.value;
            fetch(`/data.html?max_limit=${maxLimit}&scale=${temperatureScale}`, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
                .then(response => response.json())
                .then(data => {
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

            fetchStats(0, maxLimit);
            fetchStats(1, maxLimit);
            fetchStats(2, maxLimit);
        }
    });
});

// Statistics information
function fetchStats(sensorId, maxLimit) {
	fetch(`/stats?sensor_id=${sensorId}&max_limit=${maxLimit}&scale=${temperatureScale}`)
        .then(response => response.json())
        .then(stats => {
		    // Temperature stats
		    document.getElementById(`stat-temp-high-${sensorId}`).textContent = stats.temp_high ?? 'N/A';
		    document.getElementById(`stat-temp-low-${sensorId}`).textContent = stats.temp_low ?? 'N/A';
		    document.getElementById(`stat-temp-mean-${sensorId}`).textContent = stats.temp_mean ?? 'N/A';
		    document.getElementById(`stat-temp-stddev-${sensorId}`).textContent = stats.temp_stddev ?? 'N/A';

		    // Humidity stats
		    document.getElementById(`stat-hum-high-${sensorId}`).textContent = stats.hum_high ?? 'N/A';
		    document.getElementById(`stat-hum-low-${sensorId}`).textContent = stats.hum_low ?? 'N/A';
		    document.getElementById(`stat-hum-mean-${sensorId}`).textContent = stats.hum_mean ?? 'N/A';
		    document.getElementById(`stat-hum-stddev-${sensorId}`).textContent = stats.hum_stddev ?? 'N/A';

		    // General stats (only update once, not per sensor)
		    document.getElementById(`stat-count`).textContent = stats.count ?? 'N/A';
		    document.getElementById(`stat-time-early`).textContent = stats.earliest_time ?? 'N/A';
		    document.getElementById(`stat-time-late`).textContent = stats.latest_time ?? 'N/A';
        })
        .catch(error => console.error('Error fetching stats:', error));
}



