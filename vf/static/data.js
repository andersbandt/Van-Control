
// Temperature scale preference (default to Fahrenheit)
let temperatureScale = 'f';

// Average seconds between samples, derived empirically from sensor 0's
// current stats window (loop timing isn't fixed, so we measure it rather
// than assume it).
let sampleIntervalSeconds = null;

function formatDuration(totalSeconds) {
    if (!isFinite(totalSeconds) || totalSeconds <= 0) return '…';
    const minutes = totalSeconds / 60;
    const hours = minutes / 60;
    const days = hours / 24;

    if (days >= 1) return `${days.toFixed(1)} days`;
    if (hours >= 1) return `${hours.toFixed(1)} hours`;
    if (minutes >= 1) return `${minutes.toFixed(1)} min`;
    return `${Math.round(totalSeconds)} sec`;
}

function updateSliderDuration() {
    if (!sliderDuration) return;
    if (!sampleIntervalSeconds) {
        sliderDuration.textContent = '…';
        return;
    }
    sliderDuration.textContent = formatDuration(slider.value * sampleIntervalSeconds);
}

// ── Sensor naming ────────────────────────────────────────────────────────────

function applySensorNames(names) {
    Object.entries(names).forEach(([id, name]) => {
        document.querySelectorAll(`.sensor-name[data-sensor="${id}"]`).forEach(el => {
            el.textContent = name;
        });

        const trendOption = document.getElementById(`trend-opt-${id}`);
        if (trendOption) trendOption.textContent = `${name} (Sensor ${id})`;
    });

    [chart1, chart2].forEach(chart => {
        if (!chart) return;
        chart.data.datasets.forEach((ds, i) => {
            if (names[i]) ds.label = names[i];
        });
        chart.update();
    });
}

function fetchSensorNames() {
    return fetch('/sensor_names')
        .then(r => r.json())
        .then(names => {
            applySensorNames(names);
            return names;
        })
        .catch(err => console.error('Error fetching sensor names:', err));
}

// Fetch chart data and statistics on page load
window.addEventListener('DOMContentLoaded', () => {
    fetchSensorNames();

    sliderValue.textContent = slider.value;
    const initialMaxLimit = slider.value || 5000;

    // Populate charts asynchronously so the page shell loads immediately
    fetch(`/data.html?max_limit=${initialMaxLimit}&scale=${temperatureScale}`, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
        .then(r => r.json())
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
        .catch(err => console.error('Error fetching initial chart data:', err));

    fetchStats(0, initialMaxLimit);
    fetchStats(1, initialMaxLimit);
    fetchStats(2, initialMaxLimit);
});


// Update the value display when the slider changes
slider.addEventListener('input', function () {
    sliderValue.textContent = slider.value;
    updateSliderDuration();
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
            document.getElementById(`stat-temp-range-${sensorId}`).textContent = stats.temp_range ?? 'N/A';

            // Humidity stats
            document.getElementById(`stat-hum-high-${sensorId}`).textContent = stats.hum_high ?? 'N/A';
            document.getElementById(`stat-hum-low-${sensorId}`).textContent = stats.hum_low ?? 'N/A';
            document.getElementById(`stat-hum-mean-${sensorId}`).textContent = stats.hum_mean ?? 'N/A';
            document.getElementById(`stat-hum-stddev-${sensorId}`).textContent = stats.hum_stddev ?? 'N/A';
            document.getElementById(`stat-hum-range-${sensorId}`).textContent = stats.hum_range ?? 'N/A';

            // General stats reflect sensor 0 only — see fetchStats() for why.
            if (sensorId === 0) {
                document.getElementById(`stat-count`).textContent = stats.count ?? 'N/A';
                document.getElementById(`stat-time-early`).textContent = stats.earliest_time ?? 'N/A';
                document.getElementById(`stat-time-late`).textContent = stats.latest_time ?? 'N/A';
            }
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

// ── Daily Trends Chart ────────────────────────────────────────────────────────

let trendsChart = null;

const trendsSensorSelect = document.getElementById('trends-sensor');
const trendsStartPicker  = document.getElementById('trends-start');
const trendsEndPicker    = document.getElementById('trends-end');
const trendsBinSelect    = document.getElementById('trends-bin');

// Default to the past 180 days, binned weekly — enough range to see seasonal trends
(function () {
    const end = new Date();
    const start = new Date();
    start.setDate(start.getDate() - 180);
    trendsEndPicker.value   = formatDateISO(end);
    trendsStartPicker.value = formatDateISO(start);
})();

function fetchTrends() {
    const sensorId  = trendsSensorSelect.value;
    const startDate = trendsStartPicker.value;
    const endDate   = trendsEndPicker.value;
    const binDays   = trendsBinSelect.value;
    if (!startDate || !endDate) return;

    fetch(`/daily_trends?sensor_id=${sensorId}&start_date=${startDate}&end_date=${endDate}&bin_days=${binDays}&scale=${temperatureScale}`)
        .then(r => r.json())
        .then(rows => {
            const labels = rows.map(r => (r.bin_start || '').slice(0, 10));
            const highs  = rows.map(r => r.temp_high);
            const lows   = rows.map(r => r.temp_low);
            const means  = rows.map(r => r.temp_mean);

            const unit = temperatureScale === 'f' ? '°F' : '°C';
            const rangeData = labels.map((_, i) => [lows[i], highs[i]]);

            if (trendsChart) {
                trendsChart.data.labels                  = labels;
                trendsChart.data.datasets[0].data        = rangeData;
                trendsChart.data.datasets[1].data        = means;
                trendsChart.options.scales.y.title.text  = `Temperature (${unit})`;
                trendsChart.update();
            } else {
                trendsChart = new Chart(document.getElementById('trends-chart'), {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [
                            {
                                label: 'Period Range (Low – High)',
                                data: rangeData,
                                backgroundColor: 'rgba(62, 149, 205, 0.35)',
                                borderColor: '#3e95cd',
                                borderWidth: 1,
                                borderSkipped: false,
                            },
                            {
                                type: 'line',
                                label: 'Period Mean',
                                data: means,
                                borderColor: '#e8762c',
                                backgroundColor: '#e8762c',
                                pointRadius: 4,
                                pointHoverRadius: 6,
                                fill: false,
                                tension: 0.3,
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            title: {
                                display: true,
                                text: 'Temperature Trends'
                            },
                            tooltip: {
                                callbacks: {
                                    label: function(ctx) {
                                        if (ctx.datasetIndex === 0) {
                                            const [lo, hi] = ctx.raw;
                                            return `Range: ${lo}${unit} – ${hi}${unit}`;
                                        }
                                        return `Mean: ${ctx.raw}${unit}`;
                                    }
                                }
                            }
                        },
                        scales: {
                            x: { title: { display: true, text: 'Period Start' } },
                            y: { title: { display: true, text: `Temperature (${unit})` } }
                        }
                    }
                });
            }
        })
        .catch(err => console.error('Error fetching daily trends:', err));
}

// Load trends on page load and wire up controls
window.addEventListener('DOMContentLoaded', fetchTrends);
trendsStartPicker.addEventListener('change', fetchTrends);
trendsEndPicker.addEventListener('change', fetchTrends);
trendsBinSelect.addEventListener('change', fetchTrends);
trendsSensorSelect.addEventListener('change', fetchTrends);

// Re-fetch trends when temperature scale changes (append to existing scale listener)
document.querySelectorAll('input[name="temp-scale"]').forEach(radio => {
    radio.addEventListener('change', fetchTrends);
});

// ── Statistics information ─────────────────────────────────────────────────────

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
		    document.getElementById(`stat-temp-range-${sensorId}`).textContent = stats.temp_range ?? 'N/A';

		    // Humidity stats
		    document.getElementById(`stat-hum-high-${sensorId}`).textContent = stats.hum_high ?? 'N/A';
		    document.getElementById(`stat-hum-low-${sensorId}`).textContent = stats.hum_low ?? 'N/A';
		    document.getElementById(`stat-hum-mean-${sensorId}`).textContent = stats.hum_mean ?? 'N/A';
		    document.getElementById(`stat-hum-stddev-${sensorId}`).textContent = stats.hum_stddev ?? 'N/A';
		    document.getElementById(`stat-hum-range-${sensorId}`).textContent = stats.hum_range ?? 'N/A';

		    // General stats reflect sensor 0 only — the three sensors don't necessarily
		    // share the exact same count/time range (dropped DHT readings, etc.), and
		    // this keeps the displayed range consistent with the slider's duration
		    // estimate below rather than showing whichever sensor's fetch resolves last.
		    if (sensorId === 0) {
		        document.getElementById(`stat-count`).textContent = stats.count ?? 'N/A';
		        document.getElementById(`stat-time-early`).textContent = stats.earliest_time ?? 'N/A';
		        document.getElementById(`stat-time-late`).textContent = stats.latest_time ?? 'N/A';

		        // Derive the actual sample interval from sensor 0's current window so the
		        // slider's sample count can be shown as a duration.
		        if (stats.count > 1 && stats.earliest_time && stats.latest_time) {
		            const earliest = new Date(stats.earliest_time.replace(' ', 'T'));
		            const latest = new Date(stats.latest_time.replace(' ', 'T'));
		            const spanSeconds = (latest - earliest) / 1000;
		            sampleIntervalSeconds = spanSeconds / (stats.count - 1);
		            updateSliderDuration();
		        }
		    }
        })
        .catch(error => console.error('Error fetching stats:', error));
}



