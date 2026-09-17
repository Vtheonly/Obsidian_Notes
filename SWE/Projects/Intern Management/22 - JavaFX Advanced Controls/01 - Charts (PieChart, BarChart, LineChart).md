---
tags: [concept, javafx, charts, visualization]
type: concept
status: complete
related:
  - [[09 - Normalization/03 - Denormalization]]
  - [[12 - Advanced Database Features/06 - Materialized Views]]
---

# Charts (PieChart, BarChart, LineChart)

## PieChart

```java
ObservableList<PieChart.Data> data = FXCollections.observableArrayList(
    new PieChart.Data("Pending", 50),
    new PieChart.Data("Accepted", 30),
    new PieChart.Data("Rejected", 20)
);
PieChart chart = new PieChart(data);
chart.setTitle("Intern Status");
```

## BarChart

```java
CategoryAxis xAxis = new CategoryAxis();
NumberAxis yAxis = new NumberAxis();
BarChart<String, Number> chart = new BarChart<>(xAxis, yAxis);

XYChart.Series<String, Number> series = new XYChart.Series<>();
series.setName("Interns");
series.getData().addAll(
    new XYChart.Data<>("Dept 1", 30),
    new XYChart.Data<>("Dept 2", 25),
    new XYChart.Data<>("Dept 3", 40)
);
chart.getData().add(series);
```

## LineChart

```java
XYChart.Series<Number, Number> series = new XYChart.Series<>();
for (int i = 0; i < data.size(); i++) {
    series.getData().add(new XYChart.Data<>(i, data.get(i)));
}
lineChart.getData().add(series);
```

## Live updates

```java
// Bind chart data to an ObservableList — chart updates automatically
chart.setData(internService.getStatusCounts());  // ObservableList<PieChart.Data>
```

## Project Connection

The project's PieCharts use **hardcoded data**:
```java
new PieChart.Data("Department 3", 33),
new PieChart.Data("Department 2", 20),
new PieChart.Data("Department 1", 17),
new PieChart.Data("Department 1", 30)  // duplicate key!
```

The fix: query the DB (or a Materialized View):
```java
List<DepartmentCount> counts = internService.countByDepartment();
ObservableList<PieChart.Data> data = FXCollections.observableArrayList(
    counts.stream()
        .map(c -> new PieChart.Data(c.getDepartmentName(), c.getCount()))
        .collect(Collectors.toList())
);
chart.setData(data);
```

Use a Materialized View for O(1) dashboard queries. See [[12 - Advanced Database Features/06 - Materialized Views]].

## Further reading

- JavaFX Charts tutorial.
