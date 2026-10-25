---
title: "Fortune v1.0"
date: "2020-12-16T10:50:24Z"
slug: "fortune-v1-0"
categories: ["java", "technical"]
tags: ["fortune", "query"]
aliases: ["/wps/2020/12/16/fortune-v1-0/"]
wp_id: 1178
---

In one of recent discussions `with Mr. X` I was asked about my approach to solving the Linux cookie problem

1. A random quote
2. Repository will be a text file
3. Each quote will be segregated by a `'%'`
4. Can be multiline.

I always believe in incremental steps so here is what I could think of

- Read the File for the DB
- Parse each line and merge or drop as required for `'%`'.
- randomization can be an external factor - but that is step 2.

## Read DB

The final class looks like something below

```text
public class FortuneTeller {
    private final Logger logger = Logger.getLogger(FortuneTeller.class.getName());

    private List<String> allData = new LinkedList<String>();

    public FortuneTeller(File dbFile) {
        this.dbFile = dbFile;
    }

    private File dbFile;

    public FortuneTeller() {
        this(null);
        logger.log(Level.WARNING, "empty initialization");
    }

    public void populateDB() {
        this.populateDB(this.dbFile);
    }

    /**
     * Read the complete data.
     * @param localFile
     */
    public void populateDB(File localFile) {
        if (localFile == null ){
            throw new IllegalArgumentException("NO FILE SPECIFIED: file name is invalid");
        }

        if ( localFile.exists()) {
            System.out.println( " File found ");
            try {
                /**
                 * https://docs.oracle.com/javase/7/docs/api/java/nio/file/Files.html
                 */
                List<String> allLines = Files.readAllLines(localFile.toPath()).stream().collect(Collectors.toList());

                StringBuffer sb = new StringBuffer();

                for (String str: allLines) {

                    if (str.compareTo("%") != 0) {
                        sb.append(str);

                        if (allLines.indexOf(str) == allLines.size() - 1) {
                            allData.add(sb.toString() +"\n");
                            break;
                        } else {
                            sb.append("\n");
                            continue;
                        }
                    } else {
                        allData.add(sb.toString());
                        sb.setLength(0);
                    }
                }
                return;
            } catch (IOException e) {
                throw new InternalError("something went wrong");
            }
        } else {
            System.out.println("file not found: " + localFile.getPath());
        }
    }

    public String myFortune(int index) {
        if (allData.size() == 0) {
            System.out.println("no data in the system");
            throw new InternalError("no data in the system");
        }
        return allData.get(index%allData.size()).toString();
    }
}
```

### DB population: `populateDB`

```text
public void populateDB(File localFile) {
        if (localFile == null ){
            throw new IllegalArgumentException("NO FILE SPECIFIED: file name is invalid");
        }

        if ( localFile.exists()) {
            System.out.println( " File found ");
            try {
                List<String> allLines = Files.readAllLines(localFile.toPath()).stream().collect(Collectors.toList());

                StringBuffer sb = new StringBuffer();

                for (String str: allLines) {

                    if (str.compareTo("%") != 0) {
                        sb.append(str);

                        if (allLines.indexOf(str) == allLines.size() - 1) {
                            allData.add(sb.toString() +"\n");
                            break;
                        } else {
                            sb.append("\n");
                            continue;
                        }
                    } else {
                        allData.add(sb.toString());
                        sb.setLength(0);
                    }
                }
                return;
            } catch (IOException e) {
                throw new InternalError("something went wrong");
            }
        } else {
            System.out.println("file not found: " + localFile.getPath());
        }
    }
```

- If the file-argument is null Throw `illegalArgumentException`
- Read all the files 'no explicit` skipping

```text
Files.readAllLines(localFile.toPath()).stream().collect(Collectors.toList());
```

Once the Lines are read - time to parse each line and

- Drop all '`%`'
- All lines terminated by '`%`' will be joined by a new line character.

```text
for (String str: allLines) {

    if (str.compareTo("%") != 0) {
        sb.append(str);

        if (allLines.indexOf(str) == allLines.size() - 1) {
            allData.add(sb.toString() + "\n");
            break;
        } else {
            sb.append("\n");
            continue;
        }
    } else {
        allData.add(sb.toString());
        sb.setLength(0);
    }
}
```

Iterate through all the Lines read, and if the line is not just '`%`' we can append the next line.

At the end of the loop we will have `allData` populated with all the contents.

```text
public String myFortune(int index) {
        if (allData.size() == 0) {
            System.out.println("no data in the system");
            throw new InternalError("no data in the system");
        }
        return allData.get(index % allData.size()).toString();
}
```

### Fortune.DB

```text
My life is simple
%
Life is easier when you have the right set of people around you,
as friends and family to help you enjoy the moment.
   - Samarthya
%
S
%
Life is never that simple
```

## Test - JUNIT

```text
public class FortuneTellerTest {

    private final FortuneTeller ft = new FortuneTeller();

    @Test
    void testFT() {
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> ft.populateDB(null));
        assertEquals(ex.getMessage(), "NO FILE SPECIFIED: file name is invalid");
    }

    @Test
    void readLocal() {
        ft.populateDB(new File("/Users/ss670121/sourcebox/learn/golang/exercism/java/MissingNumber/src/test/resources/fortune.txt"));
        assertEquals(ft.myFortune(0), "My life is simple\n");
        assertEquals(ft.myFortune(1), "Life is easier when you have the right set of people around you,\n" +
                "as friends and family to help you enjoy the moment.\n" +
                "   - Samarthya\n");
        assertEquals(ft.myFortune(2), "S\n");
        assertEquals(ft.myFortune(3), "Life is never that simple\n");
    }

}
```
