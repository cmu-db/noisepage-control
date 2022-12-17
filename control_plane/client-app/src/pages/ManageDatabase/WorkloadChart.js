import React, { useState, useEffect, useRef } from "react";
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Clear from '@mui/icons-material/Clear';
import Chart from 'chart.js/auto';

const formatDate = (date) => {
  date = new Date(date);
  return date.toLocaleString('en-US', {
    hour12: false,
    month: 'numeric',
    day: 'numeric',
    hour: 'numeric',
    minute: 'numeric',
  });
};

// const labels = ["11/15, 22:30", "11/15, 22:35", "11/15, 22:40", "11/15, 22:45", "11/15, 22:50",
// "11/15, 22:55", "11/15, 23:00", "11/15, 23:05", "11/15, 23:10", "11/15, 23:15"];
// const labels = ["11/15, 00:00", "11/15, 01:00", "11/15, 02:00", "11/15, 03:00", "11/15, 04:00",
// "11/15, 05:00", "11/15, 06:00", "11/15, 07:00", "11/15, 08:00", "11/15, 09:00", "11/15, 10:00",
// "11/15, 11:00", "11/15, 12:00", "11/15, 13:00", "11/15, 14:00", "11/15, 15:00", "11/15, 16:00",
// "11/15, 17:00", "11/15, 18:00", "11/15, 19:00", "11/15, 20:00", "11/15, 21:00", "11/15, 22:00",
// "11/15, 23:00"];
const labels = ["12/15, 00:00", "12/15, 03:00", "12/15, 06:00", "12/15, 09:00", "12/15, 12:00", "12/15, 15:00", "12/15, 18:00", "12/15, 21:00",
"12/16, 00:00", "12/16, 03:00", "12/16, 06:00", "12/16, 09:00", "12/16, 12:00", "12/16, 15:00", "12/16, 18:00", "12/16, 21:00",
"12/17, 00:00", "12/17, 03:00", "12/17, 06:00", "12/17, 09:00", "12/17, 12:00", "12/17, 15:00", "12/17, 18:00", "12/17, 21:00"];

// const queryData = [30, 20, 12, 6, 6, 3, 20, 30, 60, 80, 90, 250, 500, 450, 300, 60, 30, 30, 250, 600, 120, 30, 10, 5];
const queryData = [41, 29, 52, 102, 319, 62, 471, 30, 42, 28, 51, 81, 257, 50, 422, 25, 18, 17, 46, 97, 363, 65, 525, 21];
// const queryData = [20, 6, 30, 80, 300, 40, 450, 20, 10, 3, 10, 15, 250, 40, 200, 10, 12, 6, 20, 450, 500, 40, 470, 20];

// const p99Data = [10.2, 11.2, 9.1, 8.2, 7.7, 12.5, 20, 20, 12, 15, 22, 200, 230, 120, 20, 10, 20, 30.5, 250, 220, 120, 30, 10, 5];
const p99Data = [14.2, 28.2, 16, 55, 122, 41, 168, 23, 9.2, 26.2, 39, 41, 114, 43, 173, 35, 32.2, 23.2, 29, 44, 133, 17, 181, 33];
// const p99Data = [10.2, 8.2, 20, 40, 120, 20, 160, 20, 10.2, 8.2, 20, 150, 200, 20, 180, 20, 10.2, 8.2, 20, 300, 250, 20, 220, 20];

const WorkloadChart = ({ workloads: workloadsProp, metricType, setSelectedWorkloadRange }) => {
  const [workloads, setWorkloads] = useState([]);
  const canvasRef = useRef(null);
  const overlayRef = useRef(null);
  const chart = useRef(null);
  const selectStartIndex = useRef(null);
  const selectStartX = useRef(0);
  const selectEndIndex = useRef(null);
  const selectionContext = useRef(null);
  const drag = useRef(false);
  const [selected, setSelected] = useState(false);

  useEffect(() => {
    setWorkloads(workloadsProp.sort(
      (a, b) => new Date(a.collected_at) - new Date(b.collected_at)
    ));

    // Prepare chart data
    // const labels = workloads.map(workload => formatDate(workload.collected_at));
    // const queries = workloads.map(workload => workload.metadata.num_queries);
    // const p99s = workloads.map(workload => workload.metadata.p99);
    const chartData = {
      // labels: labels,
      labels: labels
    }
    if (metricType === 'num_queries') {
      chartData.datasets = [{
        type: "bar",
        // data: queries
        data: queryData
      }, {
        type: "line",
        backgroundColor: "rgb(255, 99, 132)",
        borderColor: "rgb(255, 99, 132)",
        // data: queries
        data: queryData
      }];
    } else if (metricType === 'p99') {
      chartData.datasets = [{
        type: "line",
        backgroundColor: "rgb(255, 99, 132)",
        borderColor: "rgb(255, 99, 132)",
        // data: p99s
        data: p99Data
      }];
    }

    // Create chart
    const canvas = canvasRef.current;
    const canvasCtx = canvas.getContext('2d');
    chart.current = new Chart(canvasCtx, {
      data: chartData,
      options: {
        scales: {
          y: {
            title: {
              display: true,
              text: metricType === 'p99' ? 'P99 Latency (ms)' : 'Number of Queries'
            },
          },
        },
        plugins:{
          legend: {
            display: false,
          }
        }
      }
    });

    // Create overlay
    const overlay = overlayRef.current;
    overlay.width = canvas.width;
    overlay.height = canvas.height;
    selectionContext.current = overlay.getContext('2d');
    selectionContext.current.globalAlpha = 0.3;

    return () => {
      chart.current.destroy();
    };
  }, [workloadsProp, metricType]);

  const handlePointerDown = (event) => {
    const points = chart.current.getElementsAtEventForMode(event, 'index', {
      intersect: false
    });
    selectStartIndex.current = points[0].index;
    const rect = canvasRef.current.getBoundingClientRect();

    selectStartX.current = event.clientX - rect.left;
    drag.current = true;
    setSelected(false);
  };

  const handlePointerMove = (event) => {
    if (selected) {
      return;
    }

    const rect = canvasRef.current.getBoundingClientRect();
    if (drag.current) {
      selectionContext.current.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
      const x = (event.clientX - rect.left)
      selectionContext.current.fillRect(selectStartX.current,
        chart.current.chartArea.top,
        x - selectStartX.current,
        chart.current.chartArea.bottom - chart.current.chartArea.top
      );
    } else {
      selectionContext.current.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
      const x = event.clientX - rect.left;
      if (x > chart.current.chartArea.left) {
        selectionContext.current.fillRect(x,
          chart.current.chartArea.top,
          1,
          chart.current.chartArea.bottom - chart.current.chartArea.top
        );
      }
    }
  };

  const handlePointerUp = (event) => {
    const points = chart.current.getElementsAtEventForMode(event, 'index', {
      intersect: false
    });
    selectEndIndex.current = points[0].index;
    drag.current = false;

    if (selectStartIndex.current > selectEndIndex.current) {
      const tmp = selectStartIndex.current;
      selectStartIndex.current = selectEndIndex.current;
      selectEndIndex.current = tmp;
    }
    console.log(selectStartIndex.current, selectEndIndex.current);
    setSelectedWorkloadRange([labels[selectStartIndex.current], labels[selectEndIndex.current]]);
    setSelected(true);
  };

  const handleClearSelection = () => {
    setSelected(false);
    setSelectedWorkloadRange(null);
    selectionContext.current.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
  };

  return (
    <Box align="center" sx={{ position: 'relative', overflow: 'hidden' }}>
      <canvas ref={overlayRef} id="workloadChartOverlay"
        style={{
          position: 'absolute',
          pointerEvents: 'none',
          top: 0,
          left: 0,
        }}
      ></canvas>
      <canvas ref={canvasRef} id="workloadChartContainer"
        onPointerDown={handlePointerDown}
        onPointerMove={handlePointerMove}
        onPointerUp={handlePointerUp}
      ></canvas>
      {selected &&
        <Typography
          color={'error.main'}
          component="div"
          sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mt: 3 }}
        >
          Selected Range: {`${labels[selectStartIndex.current]} ~ ${labels[selectEndIndex.current]}`}
          <Button
            startIcon={<Clear sx={{ m: 0 }}/>}
            variant='outlined'
            color='error'
            sx={{ ml: 2 }}
            onClick={handleClearSelection}
          >
            Clear
          </Button>
        </Typography>
      }
    </Box>
  );
};

export default WorkloadChart;
