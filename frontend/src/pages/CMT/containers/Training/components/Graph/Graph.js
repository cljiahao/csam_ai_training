import React, { useContext } from "react";
import { LineChart } from "@mui/x-charts";
import { AppContext } from "../../../../../../contexts/context";

const Graph = () => {
  const { graph } = useContext(AppContext);

  const keyToLabel = {
    accuracy: "Accuracy",
    val_accuracy: "Validation Accuracy",
    loss: "Loss",
    val_loss: "Validation Loss",
  };

  const colors = {
    accuracy: "lightgreen",
    val_accuracy: "yellow",
    loss: "lightblue",
    val_loss: "orange",
  };

  return (
    <div className="h-full w-full shadow-lg hover:bg-amber-300 hover:bg-opacity-10">
      <LineChart
        xAxis={[
          {
            dataKey: "epoch",
            label: "Epoch",
            valueFormatter: (v) => v.toString(),
            tickMinStep: 1,
          },
        ]}
        yAxis={[
          { id: "left", label: "Accuracy", tickMinStep: 0.1 },
          { id: "right", label: "Losses", tickMinStep: 0.1 },
        ]}
        series={Object.keys(keyToLabel).map((key) => {
          const yAxis = key.includes("accuracy") ? "left" : "right";
          return {
            yAxisKey: yAxis,
            dataKey: key,
            label: keyToLabel[key],
            color: colors[key],
            showMark: false,
          };
        })}
        dataset={graph.graph}
        rightAxis="right"
        slotProps={{
          legend: {
            direction: "row",
            position: { vertical: "top", horizontal: "middle" },
            padding: 0,
            itemMarkWidth: 15,
            itemMarkHeight: 15,
            markGap: 15,
            itemGap: 50,
          },
        }}
      />
    </div>
  );
};

export default Graph;
