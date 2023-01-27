#resets the hourly count, this is called by a cron job
with open("./hourly_count.txt", "w") as file:
    file.write("0")