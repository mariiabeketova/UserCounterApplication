**TABLE UPDATE TESTS:**

Number of updates per 1 thread = 10 000

Number of threads = 10

_Results:_

|     | **DELTA (seconds)** | **LAST counter value** |
| --- | --- | --- |
| **_1\. Lost-update test_** | 25.8939 | 10 581 |
| **_2\. In-place update test_** | 23.8539 | 100 001 |
| **_3\. Row-level locking test_** | 38.5729 | 100 001 |
| **_4\. Optimistic concurrency control test_** | 182.1849 | 100 001 |