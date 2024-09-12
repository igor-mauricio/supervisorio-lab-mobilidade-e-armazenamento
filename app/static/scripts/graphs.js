let width, height, gradient;
    function getGradient(ctx, chartArea) {
    const chartWidth = chartArea.right - chartArea.left;
    const chartHeight = chartArea.bottom - chartArea.top;
    if (!gradient || width !== chartWidth || height !== chartHeight) {
        // Create the gradient because this is either the first render
        // or the size of the chart has changed
        width = chartWidth;
        height = chartHeight;
        gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
        gradient.addColorStop(0, '#7C3AED00');
        // gradient.addColorStop(0.4, '#FFFF00');
        gradient.addColorStop(1, '#7C3AED');
    }

    return gradient;
}

function newGraph(context){
    return new Chart(context, {
        type: 'line',
        data: {
          labels: [], // Initialize with empty labels
          datasets: [{
            data: [], // Initialize with empty data
            borderWidth: 1,
            fill: true,
            pointStyle: 'circle',
            pointRadius: 2,
            pointHoverRadius: 5,
            cubicInterpolationMode: 'monotone',
            backgroundColor: function(context) {
              const chart = context.chart;
              const {ctx, chartArea} = chart;
  
              if (!chartArea) {
                // This case happens on initial chart load
                return;
              }
              return getGradient(ctx, chartArea);
            },
            borderColor: '#7C3AED'
          }]
        },
        options: {
          animation:false,
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                color: '#AAAAAA'
              },
            },
            x: {
              ticks: {
                color: '#AAAAAA'
              }
            }
          },
          plugins: {
            legend: {
              display: false, // Hide the legend
            }
          }
        }
      });
}