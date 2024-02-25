**TABLE UPDATE TESTS:**

Number of updates per 1 thread = 10 000

Number of threads = 10

_Results:_

|     | **DELTA (seconds)** | **LAST counter value** |
| --- | --- | --- |
| **_1\. Lost-update test_** | 184.4098 | 10 000 |
| **_2\. In-place update test_** | 190.5284 | 100 001 |
| **_3\. Row-level locking test_** | 211.6444 | 100 001 |
| **_4\. Optimistic concurrency control test_** | 1475.4117 | 100 001 |