function FloorPlanCanvas(container, args) {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    container.appendChild(canvas);
    const zoomIn = document.getElementById('zoom-in');
    const zoomOut = document.getElementById('zoom-out');
    let transformation_matrix = [1, 0, 0, 1, 0, 0];
    let zoom_factor = 1;
    let max_zoom = 10;
    let min_zoom = 0.1;
    const scroll_sensitivity = 0.0005;
    const camera_offset = { x: 0, y: 0 };
    const drag_info = { dragging: false, start_x: 0, start_y: 0, offset_x: 0, offset_y: 0, matrix: transformation_matrix };
    const hammer = new Hammer(canvas);
    const self = this;
    const bodyStyles = window.getComputedStyle(document.body);
    const fontFamily = bodyStyles.getPropertyValue('font-family');
    const fontStyle = bodyStyles.getPropertyValue('font-style');

    this.fp_first_draw = true;
    this.floor_plan_img = undefined;
    this.floor_plan_img_size = { width: 0, height: 0 };
    this.default_cursor = 'default';
    this.ctx = ctx;
    this.canvas = canvas;
    this.markers = [];
    this.show_sensor_value = true;
    this.show_sensor_alert = true;
    this.marker_on_hover = undefined;
    this.marker_on_click = undefined;
    this.marker_on_dbl_click = undefined;
    this.on_right_click = undefined;
    this.on_zoom = undefined;
    this.on_drag = undefined;

    // Initialize
    this.set_markers(args.markers);
    this.set_show_sensor_value(args.show_sensor_value);
    this.set_show_sensor_alert(args.show_sensor_alert);
    this.set_marker_on_hover(args.marker_on_hover);
    this.set_marker_on_click(args.marker_on_click);
    this.set_marker_on_dbl_click(args.marker_on_dbl_click);
    this.set_on_right_click(args.on_right_click);
    this.set_on_zoom(args.on_zoom);
    this.set_on_drag(args.on_drag);

    if(args.img_url) {
        this.set_img_from_url(args.img_url);
    } else if(args.img) {
        this.set_img(args.img);
    }

    function translate(x,y){
        transformation_matrix[4] += transformation_matrix[0] * x + transformation_matrix[2] * y;
        transformation_matrix[5] += transformation_matrix[1] * x + transformation_matrix[3] * y;
        ctx.translate(x,y);
    }

    function scale(x,y){
        transformation_matrix[0] *= x;
        transformation_matrix[1] *= x;
        transformation_matrix[2] *= y;
        transformation_matrix[3] *= y;
        ctx.scale(x,y);
    }

    function resize(width, height) {
        canvas.width = width;
        canvas.height = height;
        transformation_matrix = [1, 0, 0, 1, 0, 0];
    }

    function get_coords_relative_to_container(x, y, matrix) {
        return {
            x: x * matrix[0] + y * matrix[2] + matrix[4],
            y: x * matrix[1] + y * matrix[3] + matrix[5]
        };
    }

    function get_coords_relative_to_image(x, y, matrix) {
        let det = matrix[0] * matrix[3] - matrix[1] * matrix[2];
        return {
            x: (x * matrix[3] - y * matrix[2] + matrix[2] * matrix[5] - matrix[3] * matrix[4]) / det,
            y: (-x * matrix[1] + y * matrix[0] - matrix[0] * matrix[5] + matrix[1] * matrix[4]) / det
        };
    }

    function zoom(factor) {
        const center_x = canvas.width / 2;
        const center_y = canvas.height / 2;
        // set zoom point to center of canvas
        translate(center_x, center_y);
        scale(factor, factor);
        // reset coordinates to original position
        translate(-center_x, -center_y);
    }

    function pan(x, y) {
        translate(x, y);
    }

    function set_image_border(color){
        ctx.save();
        ctx.strokeStyle = color;
        ctx.lineWidth = 2;
        ctx.strokeRect(0, 0, self.floor_plan_img_size.width, self.floor_plan_img_size.height);
        ctx.restore();
    }

    function draw() {
        const containerRect = container.getBoundingClientRect();
        const containerWidth = containerRect.width;
        const containerHeight = containerRect.height;
        // set to container size
        resize(containerWidth, containerHeight);
        // clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        // wait for image to load
        if(image_is_loaded_and_valid(self.floor_plan_img)) {
            if(self.fp_first_draw) {
                self.fp_first_draw = false;
                // set zoom to fit the image in the container
                if(containerHeight < self.floor_plan_img.height || containerWidth < self.floor_plan_img.width) {
                    zoom_factor = Math.min(containerHeight / self.floor_plan_img.height, containerWidth / self.floor_plan_img.width);
                    zoom(zoom_factor);
                    // Bring back to top
                    const coords = get_coords_relative_to_container(camera_offset.x, camera_offset.y, transformation_matrix);
                    camera_offset.x = -coords.x / zoom_factor;
                    camera_offset.y = -coords.y / zoom_factor;
                    pan(camera_offset.x, camera_offset.y);
                }
                // Center in canvas
                const img_width = self.floor_plan_img.width;
                const img_height = self.floor_plan_img.height;
                const scaled_img_height = img_height * zoom_factor;
                const scaled_img_width = img_width * zoom_factor;
                const x_offset = (containerWidth - scaled_img_width) / 2;
                const y_offset = (containerHeight - scaled_img_height) / 2;
                camera_offset.x += x_offset / zoom_factor;
                camera_offset.y += y_offset / zoom_factor;
                pan(camera_offset.x, camera_offset.y);
                ctx.drawImage(self.floor_plan_img, 0, 0);
                self.floor_plan_img_size = {width: self.floor_plan_img.width, height: self.floor_plan_img.height};
                set_image_border('lightgray');
            } else {
                // set zoom
                zoom(zoom_factor);
                // set pan
                pan(camera_offset.x, camera_offset.y);
                // drw image
                ctx.drawImage(self.floor_plan_img, 0, 0);
                set_image_border('lightgray');
                // draw markers
                if (self.markers) {
                    self.markers.forEach(marker => {
                        marker.fp_coords = {
                            x: marker.x * self.floor_plan_img.width,
                            y: marker.y * self.floor_plan_img.height,
                            transformation_matrix,
                        };
                        draw_marker(marker);
                    });
                }
            }
        }
        requestAnimationFrame(draw);
    }

    function draw_marker(marker) {
        if(!isNaN(marker.fp_coords.x) && !isNaN(marker.fp_coords.y)) {
            const icon_scale = isNaN(marker.icon_scale) ? 1 : marker.icon_scale;
            const marker_x = marker.fp_coords.x;
            const marker_y = marker.fp_coords.y;
            if(image_is_loaded_and_valid(marker.icon_img)) {
                const width = marker.icon_img.width * icon_scale;
                const height = marker.icon_img.height * icon_scale;
                const x = (marker_x - width / 2);
                const y = (marker_y - height / 2);
                set_marker_computed_values(marker, x, y, width, height);
                draw_marker_icon(marker, x, y, width, height);
                if(marker.img_reload) {
                    marker.img_reload = false;
                    marker.icon_img = new Image();
                    marker.icon_img.src = marker.icon;
                }
            } else {
                const default_icon_width = 20;
                const default_icon_height = 20;
                const width = default_icon_width;
                const height = default_icon_height;
                const x = (marker_x - width / 2);
                const y = (marker_y - height / 2);
                set_marker_computed_values(marker, x, y, width, height);
                draw_default_marker_icon(marker, x, y, width, height);
                if(marker.icon && (marker.img_reload || !marker.icon_img || marker.icon_img.src !== marker.icon)) {
                    marker.img_reload = false;
                    marker.icon_img = new Image();
                    marker.icon_img.src = marker.icon;
                }
            }
        }
    }

    function set_marker_computed_values(marker, x, y, width, height) {
        const top_left = get_coords_relative_to_container(x, y, transformation_matrix);
        const bottom_right = get_coords_relative_to_container(x + width, y + height, transformation_matrix);
        marker.canvas_points = { x1: top_left.x, y1: top_left.y, x2: bottom_right.x, y2: bottom_right.y };
        marker.rect = { x, y, width, height };
    }

    function draw_marker_icon(marker, x, y, width, height) {
        ctx.save();
        set_marker_draw_style(marker);
        ctx.drawImage(marker.icon_img, x, y, width, height);
        draw_marker_text(marker, x, y, width, height);
        ctx.restore();
    }

    function draw_default_marker_icon(marker, x, y, width, height) {
        ctx.save();
        set_marker_draw_style(marker);
        ctx.beginPath();
        ctx.arc(x + width / 2, y + width / 2, width / 2, 0, 2 * Math.PI);
        ctx.fillStyle = "red";
        ctx.fill();
        ctx.lineWidth = 4;
        ctx.strokeStyle = "blue";
        ctx.stroke();
        draw_marker_text(marker, x, y, width, height);
        ctx.restore();
    }

    function draw_marker_text(marker, x, y, width, height) {
        const text_size = marker.text_size || 25;
        const text_padding = text_size / 2.2;
        const gap = 5 + text_padding;

        if(marker.sensor_value && self.show_sensor_value) {
            let text_color;
            if(marker.sensor_alert) {
                text_color = 'red';
            } else {
                text_color = 'blue';
            }

            ctx.font = `${fontStyle} bold ${text_size}px ${fontFamily}`;
            const text_value = marker.sensor_value;
            const text = ctx.measureText(text_value);
            const text_height = text.actualBoundingBoxAscent + text.actualBoundingBoxDescent;
            const text_width = text.width;
            const text_y = y + height + text_height + gap;
            const text_x = x - text.width / 2 + (width / 2);
            const text_rect_x = text_x - text_padding;
            const text_rect_y = text_y - text_height - text_padding;
            const text_rect_width = text_width + text_padding * 2;
            const text_rect_height = text_height + text_padding * 2;
            ctx.fillStyle = 'white';
            ctx.strokeStyle = text_color;
            ctx.beginPath();
            ctx.roundRect(text_rect_x, text_rect_y, text_rect_width, text_rect_height, 8);
            ctx.fill();
            ctx.closePath();
            ctx.save();
            ctx.shadowBlur = 0;
            ctx.shadowOffsetX = 0;
            ctx.shadowOffsetY = 0;
            ctx.beginPath();
            ctx.roundRect(text_rect_x, text_rect_y, text_rect_width, text_rect_height, 8);
            ctx.stroke();
            ctx.closePath();
            ctx.fillStyle = text_color;
            ctx.fillText(text_value, text_x, text_y);
            ctx.restore();
        }
    }

    function set_marker_draw_style(marker) {
        ctx.shadowBlur = 9;
        ctx.shadowOffsetX = 4;
        ctx.shadowOffsetY = 4;

        if(marker.selected) {
            ctx.shadowColor = 'rgba(255,174,0,0.8)';
        } else if(marker.hover) {
            set_cursor_style('pointer');
            if(marker.sensor_alert && self.show_sensor_alert) {
                ctx.shadowColor = 'rgba(255,45,45,0.63)';
            } else {
                ctx.shadowColor = 'rgba(22,92,255,0.6)';
            }
        } else {
            if(marker.sensor_alert && self.show_sensor_alert) {
                ctx.shadowColor = 'rgba(255,0,0,0.4)';
            } else {
                ctx.shadowColor = 'rgba(0,0,0,0.4)';
            }
        }
    }

    function image_is_loaded_and_valid(img) {
        return img && img.complete && img.naturalWidth !== 0 && img.naturalHeight !== 0;
    }

    //------------ Event handlers ------------

    function get_event_location(e){
        return {
            x: e.center.x,
            y: e.center.y,
        };
    }

    function on_pan_start(e){
        e.preventDefault();
        drag_info.dragging = true;
        const location = get_event_location(e);
        drag_info.start_x = location.x/zoom_factor;
        drag_info.start_y = location.y/zoom_factor;
        drag_info.x = location.x;
        drag_info.y = location.y;
        drag_info.offset_x = camera_offset.x;
        drag_info.offset_y = camera_offset.y;
        drag_info.matrix = Array.from(transformation_matrix);
    }

    function on_pan_end(e){
        e.preventDefault();
        drag_info.dragging = false;
        drag_info.matrix = Array.from(transformation_matrix);
    }

    function on_pan_move(e){
        e.preventDefault();
        if(self.on_drag) {
            self.on_drag();
        }
        const location = get_event_location(e);
        camera_offset.x = drag_info.offset_x + (location.x/zoom_factor - drag_info.start_x);
        camera_offset.y = drag_info.offset_y + (location.y/zoom_factor - drag_info.start_y);
    }

    function set_cursor_style(style) {
        canvas.style.cursor = style;
    }

    function handle_hover(e){
        if (!drag_info.dragging) {
            const location = {
                x: e.clientX,
                y: e.clientY,
            }
            const target = get_target(location);
            for(const marker of self.markers) {
                marker.hover = false;
            }
            if(target){
                target.hover = true;
                set_cursor_style('pointer');
                if(self.marker_on_hover) {
                    self.marker_on_hover(target, e);
                }
            } else {
                set_cursor_style(self.default_cursor);
            }
        }
    }

    function handle_click(e){
        const location = get_event_location(e);
        const target = get_target(location);
        if(self.marker_on_click) {
            self.marker_on_click(target, e);
        }
    }

    function handle_right_click(e){
        e.preventDefault();
        const location = {
            x: e.clientX,
            y: e.clientY,
        };
        const target = get_target(location);
        const image_location = get_image_coords(location);
        if(self.on_right_click) {
            self.on_right_click(target, image_location, e);
        }
    }

    function handle_dbl_click(e){
        const location = get_event_location(e);
        const target = get_target(location);
        if(self.marker_on_dbl_click) {
            self.marker_on_dbl_click(target, e);
        }
    }

    function get_target(location) {
        const image_location = get_image_coords(location);
        if(image_location){
            if(self.markers){
                for(const marker of self.markers){
                    if(marker.rect) {
                        const { x, y, width, height } = marker.rect;
                        const x1 = x;
                        const y1 = y;
                        const x2 = x + width;
                        const y2 = y + height;
                        if (image_location.x >= x1 && image_location.x <= x2 && image_location.y >= y1 && image_location.y <= y2) {
                            return marker;
                        }
                    }
                }
            }
        }
    }

    function adjust_zoom(e, amount, factor){
        e.preventDefault();
        if (!drag_info.dragging){
            if(self.on_zoom) {
                self.on_zoom();
            }
            let zoom_update = undefined;
            if (amount){
                zoom_update = zoom_factor + amount;
            } else if (factor){
                zoom_update = factor * zoom_factor;
            }

            if(zoom_update){
                zoom_factor = Math.min(Math.max(zoom_update, min_zoom), max_zoom);
            }
        }
    }

    function get_image_coords(location){
        const rect = canvas.getBoundingClientRect();
        const x = (location.x - rect.left);
        const y = (location.y - rect.top);
        const coords = get_coords_relative_to_image(x, y, transformation_matrix);
        if(coords.x >= 0 && coords.x <= self.floor_plan_img_size.width && coords.y >= 0 && coords.y <= self.floor_plan_img_size.height){
            return coords;
        } else {
            return null;
        }
    }

    zoomOut.addEventListener('click', function() {
        if(zoom_factor > min_zoom) {
            if(self.on_zoom) {
                self.on_zoom();
            }
            zoom_factor = Math.max(zoom_factor - 0.1, min_zoom);
        }
    });
    zoomIn.addEventListener('click', function() {
        if(zoom_factor < max_zoom) {
            if(self.on_zoom) {
                self.on_zoom();
            }
            zoom_factor = Math.min(zoom_factor + 0.1, max_zoom);
        }
    });

    const singleTap = new Hammer.Tap({ event: "tap" });
    const doubleTap = new Hammer.Tap({ event: "doubletap", taps: 2 });

    hammer.add([doubleTap, singleTap]);

    singleTap.requireFailure(doubleTap);
    doubleTap.recognizeWith(singleTap);

    hammer.get('pan').set({direction: Hammer.DIRECTION_ALL });
    hammer.on('panstart', on_pan_start);
    hammer.on('panend', on_pan_end);
    hammer.on('panmove', on_pan_move);
    hammer.on('tap', handle_click);
    hammer.on('doubletap', handle_dbl_click);
    canvas.addEventListener('contextmenu', handle_right_click);
    canvas.addEventListener('wheel', (e) => adjust_zoom(e, e.deltaY * scroll_sensitivity))
    canvas.addEventListener('mousemove', handle_hover);
    draw();
}

FloorPlanCanvas.prototype.image = function () {
    return this.floor_plan_img;
}

FloorPlanCanvas.prototype.image_size = function () {
    return this.floor_plan_img_size;
}

FloorPlanCanvas.prototype.set_cursor = function (cursor) {
    this.default_cursor = cursor;
    this.canvas.style.cursor = cursor;
}

FloorPlanCanvas.prototype.set_img = function (img) {
    this.fp_first_draw = true;
    this.floor_plan_img_size = { width: img.width, height: img.height };
    this.floor_plan_img = img;
}

FloorPlanCanvas.prototype.set_img_from_url = function (img_url) {
    this.fp_first_draw = true;
    this.floor_plan_img = new Image();
    this.floor_plan_img.src = img_url;
}

FloorPlanCanvas.prototype.set_markers = function (markers) {
    this.markers = markers || [];
}

FloorPlanCanvas.prototype.set_marker_on_hover = function (callback) {
    this.marker_on_hover = callback;
}

FloorPlanCanvas.prototype.set_marker_on_click = function (callback) {
    this.marker_on_click = callback;
}

FloorPlanCanvas.prototype.set_marker_on_dbl_click = function (callback) {
    this.marker_on_dbl_click = callback;
}

FloorPlanCanvas.prototype.set_on_right_click = function (callback) {
    this.on_right_click = callback;
}

FloorPlanCanvas.prototype.set_show_sensor_value = function (show) {
    this.show_sensor_value = show;
}

FloorPlanCanvas.prototype.set_show_sensor_alert = function (show) {
    this.show_sensor_alert = show;
}

FloorPlanCanvas.prototype.set_on_zoom = function (callback) {
    this.on_zoom = callback;
}

FloorPlanCanvas.prototype.set_on_drag = function (callback) {
    this.on_drag = callback;
}