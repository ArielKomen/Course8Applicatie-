var django = {
    "jQuery": jQuery.noConflict(true)
};
var jQuery = django.jQuery;
var $ = jQuery;

(function ($) {
    $(function () {
        $(document).ready(function () {
            // Initialize event listeners
            ru.ariel.do_visualisation();
        });
    });
})(django.jQuery);

// based on the type, action will be loaded

// var $ = django.jQuery.noConflict();

var ru = (function ($, ru) {
    "use strict";

    ru.ariel = (function ($, config) {
        // Define variables for ru.collbank here
        var arc = null,
            x = null,
            y = null,
            middleArcLine = null,
            textFits = null,
            svg = null;


        // Private methods specification
        var private_methods = {}

        // Public methods
        return {

            do_visualisation: function () {


                const width = document.getElementById("visualisatie").offsetWidth, // window.innerWidth,
                    height = document.getElementById("visualisatie").offsetHeight, // window.innerHeight,
                    maxRadius = (Math.min(width, height) / 2) - 5;

                const formatNumber = d3.format(',d');

                x = d3.scaleLinear()
                    .range([0, 2 * Math.PI])
                    .clamp(true);

                y = d3.scaleSqrt()
                    .range([maxRadius * .1, maxRadius]);

                const color = d3.scaleOrdinal(d3.schemeCategory20);

                const partition = d3.partition();

                arc = d3.arc()
                    .startAngle(d => x(d.x0))
                    .endAngle(d => x(d.x1))
                    .innerRadius(d => Math.max(0, y(d.y0)))
                    .outerRadius(d => Math.max(0, y(d.y1)));

                middleArcLine = d => {
                    const halfPi = Math.PI / 2;
                    const angles = [x(d.x0) - halfPi, x(d.x1) - halfPi];
                    const r = Math.max(0, (y(d.y0) + y(d.y1)) / 2);

                    const middleAngle = (angles[1] + angles[0]) / 2;
                    const invertDirection = middleAngle > 0 && middleAngle < Math.PI; // On lower quadrants write text ccw
                    if (invertDirection) {
                        angles.reverse();
                    }

                    const path = d3.path();
                    path.arc(0, 0, r, angles[0], angles[1], invertDirection);
                    return path.toString();
                };

                textFits = d => {
                    const CHAR_SPACE = 6;

                    const deltaAngle = x(d.x1) - x(d.x0);
                    const r = Math.max(0, (y(d.y0) + y(d.y1)) / 2);
                    const perimeter = r * deltaAngle;

                    return d.data.name.length * CHAR_SPACE < perimeter;
                };

                svg = d3.select('#visualisatie').append('svg')
                    .style('width', '100%')
                    .style('height', '100vh')
                    .attr('viewBox', `${-width/2} ${-height / 2} ${width} ${height}`)
                    .on('click', () => ru.ariel.focusOn()); // Reset zoom on canvas click

                var visualisatie_url = document.getElementById('visualisatie_data').innerHTML;

                d3.json(visualisatie_url, (error, root) => {
                    if (error) throw error;

                    root = d3.hierarchy(root);
                    root.sum(d => d.size);

                    const slice = svg.selectAll('g.slice')
                        .data(partition(root).descendants());

                    slice.exit().remove();

                    const newSlice = slice.enter()
                        .append('g').attr('class', 'slice')
                        .on('click', d => {
                            d3.event.stopPropagation();
                            ru.ariel.focusOn(d);
                        });

                    newSlice.append('title')
                        .text(d => d.data.name + '\n' + formatNumber(d.value));

                    newSlice.append('path')
                        .attr('class', 'main-arc')
                        .style('fill', d => color((d.children ? d : d.parent).data.name))
                        .attr('d', arc);

                    newSlice.append('path')
                        .attr('class', 'hidden-arc')
                        .attr('id', (_, i) => `hiddenArc${i}`)
                        .attr('d', middleArcLine);

                    const text = newSlice.append('text')
                        .attr('display', d => textFits(d) ? null : 'none');

                    // Add white contour
                    text.append('textPath')
                        .attr('startOffset', '50%')
                        .attr('xlink:href', (_, i) => `#hiddenArc${i}`)
                        .text(d => d.data.name)
                        .style('fill', 'none')
                        .style('stroke', '#fff')
                        .style('stroke-width', 5)
                        .style('stroke-linejoin', 'round');

                    text.append('textPath')
                        .attr('startOffset', '50%')
                        .attr('xlink:href', (_, i) => `#hiddenArc${i}`)
                        .text(d => d.data.name);
                });
            },


            focusOn: function (d = {x0: 0, x1: 1, y0: 0, y1: 1}) {
                // Reset to top-level if no data point specified

                const transition = svg.transition()
                    .duration(750)
                    .tween('scale', () => {
                        const xd = d3.interpolate(x.domain(), [d.x0, d.x1]),
                            yd = d3.interpolate(y.domain(), [d.y0, 1]);
                        return t => {
                            x.domain(xd(t));
                            y.domain(yd(t));
                        };
                    });

                transition.selectAll('path.main-arc')
                    .attrTween('d', d => () => arc(d));

                transition.selectAll('path.hidden-arc')
                    .attrTween('d', d => () => middleArcLine(d));

                transition.selectAll('text')
                    .attrTween('display', d => () => textFits(d) ? null : 'none');

                moveStackToFront(d);

                //

                function moveStackToFront(elD) {
                    svg.selectAll('.slice').filter(d => d === elD)
                        .each(function (d) {
                            this.parentNode.appendChild(this);
                            if (d.parent) {
                                moveStackToFront(d.parent);
                            }
                        })
                }
            }
        };
    }($, ru.config));

    return ru;
}(jQuery, window.ru || {})); // window.ru: see http://stackoverflow.com/questions/21507964/jslint-out-of-scope


//document.addEventListener("DOMContentLoaded", do_visualisation);

