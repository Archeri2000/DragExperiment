from IPostProcess import PostProcess

def write(n, m):
	p.record(n, m)


def end():
	p.terminate()


p = PostProcess()
for i in range(1000):
	write(i, 3*i)
end()

