from resolver  import Resolver
from timeit import timeit 

resolve = Resolver()
 
time_elapsed = timeit(setup='from __main__ import resolve ',
                      stmt ='resolve("google.com")',number =1)
print("Time elapsed for google.com:{0:f}".format(time_elapsed))
 
time_elapsed = timeit(setup='from __main__ import resolve ',
                      stmt ='resolve("google.com")',number =1)
print("Time elapsed for google.com:{0:f}".format(time_elapsed))

print("Is microsoft.com present in resolve cache:{0}"
       .format(resolve.has_host("microsoft.com")))

resolve("microsoft.com")

print("Is microsoft.com present in resolve cache:{0}"
       .format(resolve.has_host("microsoft.com")))

resolve.clear()
print("Is microsoft.com present in resolve cache:{0}"
       .format(resolve.has_host("microsoft.com")))
