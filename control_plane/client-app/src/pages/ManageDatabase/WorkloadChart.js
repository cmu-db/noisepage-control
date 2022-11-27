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

const labels = ["11/15, 22:30", "11/15, 22:35", "11/15, 22:40", "11/15, 22:45", "11/15, 22:50",
"11/15, 22:55", "11/15, 23:00", "11/15, 23:05", "11/15, 23:10", "11/15, 23:15"];

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
        data: [100, 400, 1000, 800, 900, 20, 80, 200, 500, 10]
      }, {
        type: "line",
        backgroundColor: "rgb(255, 99, 132)",
        borderColor: "rgb(255, 99, 132)",
        // data: queries
        data: [100, 400, 1000, 800, 900, 20, 80, 200, 500, 10]
      }];
    } else if (metricType === 'p99') {
      chartData.datasets = [{
        type: "line",
        backgroundColor: "rgb(255, 99, 132)",
        borderColor: "rgb(255, 99, 132)",
        // data: p99s
        data: [60, 80, 100, 120, 90, 40, 200, 300, 70, 30]
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
