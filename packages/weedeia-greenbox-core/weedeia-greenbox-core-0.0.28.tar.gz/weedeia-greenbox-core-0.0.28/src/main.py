from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
import signal
import sys
import uvicorn

from .util.errors import ComponentError
from .pin.gpio import gpio
from .service.lightMotor import lightMotorService, MoveToRequest
from .service.systemInfo import systemInfoService

def handle_exit(_signal, _frame):
    gpio.cleanUp()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)

app = FastAPI()

@app.get("/management/status")
def health_check():
  return "UP"

@app.put("/ready-light/{active}")
def setReadyLight(active : str):
  gpio.set_ReadyLight(active)
  return Response(status_code=204)

@app.put("/cultivation-light/{active}")
def setCultivationLight(active : str):
  gpio.set_cultivationLight(active)
  return Response(status_code=204)

@app.put("/air-conditioning/{active}")
def setAirConditioning(active : str):
  gpio.set_air_conditioning(active)
  return Response(status_code=204)

@app.put("/irrigator/{active}")
def setIrrigator(active : str):
  gpio.set_irrigator(active)
  return Response(status_code=204)

@app.put("/humidifier/{active}")
def set_humidifier(active : str) :
   gpio.set_humidifier(active)
   return Response(status_code=204)

@app.put("/extractor-fan/{active}")
def set_extractorFan(active: str):
  gpio.set_extratorFan(active)
  return Response(status_code=204)

@app.put("/ventilation/{power}")
def set_ventilation(power: int):
  gpio.set_ventilation(power)
  return Response(status_code=204)

@app.put("/light-motor/reset")
def set_lightMotorResetPositon() :
  lightMotorService.reset()
  return Response(status_code=204)
  
@app.put("/light-motor/move-to")
def set_lightMotorMoveTo(request : MoveToRequest) :
  lightMotorService.move_to(request)
  return Response(status_code=204)

@app.get("/sensors")
def read_sensors():
  return systemInfoService.get_data()

@app.exception_handler(ComponentError)
async def component_exception_handler(_req, exc: ComponentError) :
  return JSONResponse(status_code= exc.httpCode, content={
    "code" : exc.errorMessage
  })

def main():
  gpio.setup()
  uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()