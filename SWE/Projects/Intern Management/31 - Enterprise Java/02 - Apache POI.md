---
tags: [concept, enterprise, excel, poi]
type: concept
status: complete
---

# Apache POI

## What it is

**Apache POI** is a Java library for reading and writing Microsoft Office documents (Excel, Word, PowerPoint).

## Maven

```xml
<dependency>
    <groupId>org.apache.poi</groupId>
    <artifactId>poi-ooxml</artifactId>
    <version>5.2.4</version>
</dependency>
```

## Writing Excel

```java
Workbook wb = new XSSFWorkbook();
Sheet sheet = wb.createSheet("Interns");

// Header
Row header = sheet.createRow(0);
header.createCell(0).setCellValue("ID");
header.createCell(1).setCellValue("Name");
header.createCell(2).setCellValue("Email");
header.createCell(3).setCellValue("Status");

// Data
for (int i = 0; i < interns.size(); i++) {
    Row row = sheet.createRow(i + 1);
    row.createCell(0).setCellValue(interns.get(i).getId());
    row.createCell(1).setCellValue(interns.get(i).getName());
    row.createCell(2).setCellValue(interns.get(i).getEmail());
    row.createCell(3).setCellValue(interns.get(i).getStatus().toString());
}

// Auto-size columns
for (int i = 0; i < 4; i++) sheet.autoSizeColumn(i);

try (FileOutputStream out = new FileOutputStream("interns.xlsx")) {
    wb.write(out);
}
```

## Reading Excel

```java
try (Workbook wb = new XSSFWorkbook(new FileInputStream("interns.xlsx"))) {
    Sheet sheet = wb.getSheetAt(0);
    for (Row row : sheet) {
        long id = (long) row.getCell(0).getNumericCellValue();
        String name = row.getCell(1).getStringCellValue();
        // ...
    }
}
```

## Use case: CSV/Excel import

```java
public List<Intern> importFromExcel(File file) {
    List<Intern> interns = new ArrayList<>();
    try (Workbook wb = new XSSFWorkbook(new FileInputStream(file))) {
        Sheet sheet = wb.getSheetAt(0);
        for (Row row : sheet) {
            if (row.getRowNum() == 0) continue;  // skip header
            interns.add(new Intern(
                row.getCell(0).getStringCellValue(),
                (int) row.getCell(1).getNumericCellValue(),
                row.getCell(2).getStringCellValue()
            ));
        }
    }
    return interns;
}
```

## Project Connection

The project has no Excel support. The fix: add Apache POI as a `DocumentExporter` implementation (XLSX format). Useful for exporting intern lists and importing bulk data.

## Further reading

- Apache POI documentation.
