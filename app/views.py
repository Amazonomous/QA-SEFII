from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Device
from .extensions import db
import json
from datetime import datetime
from app.forms import DeviceForm

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    device_form = DeviceForm()

    # Check if form was submitted
    if request.method == 'POST' and device_form.validate_on_submit():
        existing_device = Device.query.filter_by(dsn=device_form.device_dsn.data).first()

        # Add device process
        if device_form.add_button.data:
            if not existing_device:
                new_device = Device(
                    assignee=current_user.username,
                    dsn=device_form.device_dsn.data,
                    program=device_form.device_program.data,
                    location_code=device_form.device_location_code.data,
                    condition=device_form.device_condition.data,
                    last_updated=datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                )
                db.session.add(new_device)
                try:
                    db.session.commit()
                    flash('Device added', category='success')
                except Exception as e:
                    db.session.rollback()
                    flash(f'An error occurred while updating the device: {str(e)}', 'error')
            else:
                flash('Device already exists', category='error')
        # Update device process
        elif device_form.update_button.data:
            if existing_device:
                if existing_device.assignee == current_user.username:
                    try:
                        existing_device.dsn=device_form.device_dsn.data
                        existing_device.location_code=device_form.device_location_code.data
                        existing_device.condition=device_form.device_condition.data
                        existing_device.last_updated=datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                        db.session.commit()
                        flash('Device updated', category='success')
                    except Exception as e:
                        db.session.rollback()
                        flash(f'An error occurred while updating the device: {str(e)}', 'error')
                else:
                    flash('You are not authorized to update this device', 'warning')
            else:
                flash('Device was not found', 'error')
                    
    # Sort devices by the currently logged in user, so they see their devices first
    user_devices = Device.query.filter_by(assignee=current_user.username).all()
    other_devices = Device.query.filter(Device.assignee != current_user.username).all()
    devices = user_devices + other_devices

    return render_template("home.html", user=current_user, device_form=device_form, devices=devices)

@views.route('/update-device', methods=['POST'])
def update_device():  
    device = json.loads(request.data)
    deviceDsn = device['dsn']
    devices = Device.query.all()

    device = Device.query.get(deviceDsn)

    device_form = DeviceForm(
        device_dsn=device.dsn,
        device_location_code=device.location_code,
        device_condition=device.condition,
        device_program=device.program
    )

    return render_template("home.html", user=current_user, device_form=device_form, devices=devices)

@views.route('/delete-device', methods=['POST'])
def delete_device():  
    device = json.loads(request.data)
    deviceDsn = device['dsn']
    device = Device.query.get(deviceDsn)
    if current_user.id == 1:
        db.session.delete(device)
        db.session.commit()
        flash('Device deleted', category='warning')
    else:
        flash('You are not authorized to remove devices', 'error')

    return jsonify({})