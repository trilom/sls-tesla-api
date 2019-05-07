#sls-tesla-api
This is most of the Tesla commands api wrapped up, and ready for you to deploy for your own use case in AWS.

## Dependencies
### Serverless
```
npm install -g serverless
```
### Docker
```
brew cask install docker
```
### AWS CLI
```
brew install awscli
```
This also needs to be configured with:
```
aws configure
```
## Running
First you need to install dependencies for serverless with:
```
npm install
```

Then simply run with:
```
sls deploy
```

You will receive an output that looks similar to this:
```
Service Information
service: sls-tesla-api
stage: dev
region: us-east-1
stack: sls-tesla-api-dev
resources: 11
api keys:
  None
endpoints:
  ANY - https://m6ifh35s2.execute-api.us-east-1.amazonaws.com/dev/{proxy+}
functions:
  vehiclesCommand: sls-tesla-api-dev-vehiclesCommand
layers:
  None
```
You will be able to invoke the api by the endpoint listed, first you will need to get the vehicle for the bearer token:
```
http post https://m6ifh35s2.execute-api.us-east-1.amazonaws.com/dev/vehicles bearer_token=abcd1234somelongshieldtoken
```
This will give you a list of vehicle id's, with this in hand, lets honk the horn:
```
http post https://m6ifh35s2.execute-api.us-east-1.amazonaws.com/dev/command/59085098204580904/honk_horn bearer_token=abcd1234somelongshieldtoken
```
Your horn should honk.

## Endpoints
```
/command/{vehicleId}/sentry_mode_off
/command/{vehicleId}/sentry_mode_on
/command/{vehicleId}/remote_steering_wheel_heater_off
/command/{vehicleId}/remote_steering_wheel_heater_on
/command/{vehicleId}/remote_seat_heater_request/{seats}/{level}
/command/{vehicleId}/set_temps/passenger/{temp}
/command/{vehicleId}/set_temps/driver/{temp}
/command/{vehicleId}/set_temps/{temp}
/command/{vehicleId}/auto_conditioning_stop
/command/{vehicleId}/auto_conditioning_start
/command/{vehicleId}/set_charge_limit/{chargeLimit}
/command/{vehicleId}/charge_max_range
/command/{vehicleId}/charge_standard
/command/{vehicleId}/charge_stop
/command/{vehicleId}/charge_start
/command/{vehicleId}/charge_port_door_close
/command/{vehicleId}/charge_port_door_open
/command/{vehicleId}/open_frunk
/command/{vehicleId}/open_trunk
/command/{vehicleId}/honk_horn
/command/{vehicleId}/flash_lights
/command/{vehicleId}/wake_up
/command/{vehicleId}/door_unlock
/command/{vehicleId}/door_lock
/vehicles
```
