import { Line, LineChart, XAxis, YAxis } from "recharts";

import {
  ChartContainer,
  ChartLegend,
  ChartLegendContent,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";

const ModelChart = ({ epoch_data }) => {
  const chartConfig = {
    accuracy: {
      label: "Accuracy",
      color: "hsl(var(--chart-1))",
    },
    val_accuracy: {
      label: "Validation Accuracy",
      color: "hsl(var(--chart-2))",
    },
    loss: {
      label: "Loss",
      color: "hsl(var(--chart-3))",
    },
    val_loss: {
      label: "Validation Loss",
      color: "hsl(var(--chart-4))",
    },
  };

  return (
    <ChartContainer
      config={chartConfig}
      className="hw-full rounded-xl shadow-lg hover:bg-amber-300 hover:bg-opacity-10"
    >
      <LineChart accessibilityLayer data={epoch_data}>
        <ChartTooltip
          cursor={false}
          content={<ChartTooltipContent hideLabel />}
        />
        <ChartLegend
          layout="horizontal"
          verticalAlign="top"
          align="center"
          content={<ChartLegendContent />}
        />
        <XAxis
          dataKey="epoch"
          tickMargin={10}
          tickFormatter={(value) => value.toString()}
          tickMinStep={1}
        />
        <YAxis
          yAxisId="left"
          minTickGap={0.1}
          domain={[0, 1.0]}
          allowDataOverflow={true}
        />
        <YAxis
          yAxisId="right"
          orientation="right"
          minTickGap={0.1}
          domain={[0, 1.0]}
          allowDataOverflow={true}
        />
        {Object.keys(chartConfig).map((key) => {
          const yAxis = key.includes("accuracy") ? "left" : "right";
          return (
            <Line
              key={key}
              yAxisId={yAxis}
              dataKey={key}
              type="natural"
              stroke={`var(--color-${key})`}
              strokeWidth={2}
              dot={false}
            />
          );
        })}
      </LineChart>
    </ChartContainer>
  );
};

export default ModelChart;
