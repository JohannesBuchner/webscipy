
import web

urls = (
  '/', 'index',
  '/sqrt', 'sqrt',
  '/sin', 'sin',
)

class index:
	def GET(self):
		#return "Hello, world!"
		i = web.input(name=None)
		render = web.template.render('templates')
		return render.greet(name=i.name if i.name is not None else "world")

class sqrt:
	def GET(self):
		i = web.input()
		render = web.template.render('templates')
		if hasattr(i, "value"):
			return render.sqrt(i.value)
		else:
			return render.ctlheader() + render.sqrtctl()
        
class sin:
	def GET(self):
		i = web.input()
		render = web.template.render('templates')
		if hasattr(i, "freq") and hasattr(i, "ampl") and hasattr(i, "phase") and hasattr(i, "offset") and hasattr(i, "noise"):
			import hashlib
			import scipy, numpy, scipy.fftpack
			import matplotlib.pyplot as plt
			
			x = numpy.linspace(0,1,100)
			h = hashlib.sha512(",".join([i.freq, i.ampl, i.phase, i.offset, i.noise]))
			i.freq = float(i.freq)
			i.ampl = float(i.ampl)
			i.offset = float(i.offset)
			i.phase = float(i.phase)
			i.noise = float(i.noise)
			y = i.offset + i.ampl * numpy.sin(i.freq * x + i.phase / 180. * numpy.pi)
			if i.noise > 0:
				y = scipy.random.normal(y, i.noise)
			
			plt.figure()
			plt.subplot(2, 1, 1)
			plt.plot(x, y, '+')
			plt.xlabel("time")
			plt.ylabel("value")
			plt.subplot(2, 1, 2)
			
			p = scipy.fftpack.fft(y)
			n = len(p)/2
			p = p[:n]**2
			f = numpy.arange(len(p)) * 1. / len(x)
			plt.plot(f, p, '+')
			plt.xlabel("frequency")
			plt.ylabel("power")
			fftfilename = "static/output/%s.png" % h.hexdigest()
			plt.savefig(fftfilename, bbox_inches='tight')
			
			return render.sin(freq=i.freq, ampl=i.ampl, phase=i.phase, offset=i.offset, noise=i.noise, fftfilename=fftfilename)
		else:
			return str(render.ctlheader()) + str(render.sinctl())
        

if __name__ == "__main__": 
	app = web.application(urls, globals())
	app.run()



