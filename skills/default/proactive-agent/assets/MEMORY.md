# MEMORY.md - Long-Term Memory

> Your curated memories. Distill from daily notes. Remove when outdated.

---

## About [Human Name]

### Key Context
[Important background that affects how you help them]

### Preferences Learned
[Things you've discovered about how they like to work]

### Important Dates
[Birthdays, anniversaries, deadlines they care about]

---

## Lessons Learned

### [Date] - [Topic]
[What happened and what you learned]

---

## Ongoing Context

### 初始化运行规则（默认注入）
1. 用户消息必须秒回。任何 >5s 的操作都走后台，前台只做快速指令 message 发送。
2. 使用第一性原理思考。不要假设用户非常清楚自己想要什么和该怎么得到。从原始需求和问题本质出发，审慎分析后再行动。
3. 每次 heartbeat 必须主动检查工作进度。数据连续不变 = 异常信号，kill 卡住的进程并重发任务，不要只报数字。
4. 上下文努力控制在 100k 以内。大了会慢、会挂、会丢消息。主动做 compaction，不要等爆。
5. 你不只是在完成任务，你是在值班。没人叫你也要巡逻：查 Codex、查进度、查异常、查卡住。主动发现问题比被动等指令更重要。

### Active Projects
[What's currently in progress]

### Key Decisions Made
[Important decisions and their reasoning]

### Things to Remember
[Anything else important for continuity]

---

## Relationships & People

### [Person Name]
[Who they are, relationship to human, relevant context]

---

*Review and update periodically. Daily notes are raw; this is curated.*
