-- Read-only Resolve 19 console audit. No UIManager, external socket, or project writes.
-- Run in Workspace > Console > Lua:
-- dofile('/absolute/path/inspect_resolve.lua')({expected_project='tommy-fox-show', output_path='/absolute/path/new-report.json'})
return function(options)
    options = options or {}
    local function array() return setmetatable({}, {json_array = true}) end
    local errors = array()
    local function get(object, method, ...)
        local args = {...}
        if not object then return nil end
        local ok, result = pcall(function() return object[method](object, unpack(args)) end)
        if not ok then
            errors[#errors + 1] = {method = method, error = tostring(result)}
            return nil
        end
        return result
    end
    local function quote(value)
        return '"' .. value:gsub('[%z\1-\31\\"]', function(c)
            if c == '"' then return '\\"' end
            if c == '\\' then return '\\\\' end
            return string.format('\\u%04x', string.byte(c))
        end) .. '"'
    end
    local function json(value)
        local kind = type(value)
        if kind == 'nil' then return 'null' end
        if kind == 'boolean' then return tostring(value) end
        if kind == 'number' then
            if value ~= value or value == math.huge or value == -math.huge then return 'null' end
            return tostring(value)
        end
        if kind == 'string' then return quote(value) end
        if kind ~= 'table' then return quote(tostring(value)) end
        local parts = {}
        if getmetatable(value) and getmetatable(value).json_array then
            for _, v in ipairs(value) do parts[#parts + 1] = json(v) end
            return '[' .. table.concat(parts, ',') .. ']'
        end
        local keys = {}
        for key in pairs(value) do keys[#keys + 1] = key end
        table.sort(keys, function(a, b) return tostring(a) < tostring(b) end)
        for _, key in ipairs(keys) do parts[#parts + 1] = quote(tostring(key)) .. ':' .. json(value[key]) end
        return '{' .. table.concat(parts, ',') .. '}'
    end

    local r = resolve or get(app, 'GetResolve') or get(fusion, 'GetResolve')
    assert(r, 'No in-process Resolve object. Run from Resolve Workspace > Console > Lua.')
    local project = get(get(r, 'GetProjectManager'), 'GetCurrentProject')
    local project_name = get(project, 'GetName')
    assert(project, 'No project is open. No project was created or loaded.')
    assert(not options.expected_project or project_name == options.expected_project,
        'Project mismatch; expected ' .. tostring(options.expected_project) .. ', found ' .. tostring(project_name))

    local report = {
        schema_version = 1,
        started_at_utc = os.date('!%Y-%m-%dT%H:%M:%SZ'),
        access = 'in_process_lua_console',
        read_only = true,
        product = get(r, 'GetProductName'),
        resolve_version = get(r, 'GetVersionString'),
        page = get(r, 'GetCurrentPage'),
        project = {name = project_name, id = get(project, 'GetUniqueId'),
            frame_rate_setting = get(project, 'GetSetting', 'timelineFrameRate'),
            width_setting = get(project, 'GetSetting', 'timelineResolutionWidth'),
            height_setting = get(project, 'GetSetting', 'timelineResolutionHeight'),
            timeline_count = get(project, 'GetTimelineCount')},
        timelines = array(), media = array(), errors = errors,
        scan_truncated = false,
        note = 'Snapshot during ingest; media counts and source availability may change.'
    }
    local limit = math.max(1, math.min(tonumber(options.max_media) or 2000, 10000))
    local visited = {}
    local function folder_scan(folder, parent, depth)
        if not folder then return end
        if depth > 30 then report.scan_truncated = true; return end
        local id = get(folder, 'GetUniqueId') or tostring(folder)
        if visited[id] then return end
        visited[id] = true
        local name = get(folder, 'GetName') or '?'
        local path = parent == '' and name or parent .. '/' .. name
        for _, clip in ipairs(get(folder, 'GetClipList') or {}) do
            if #report.media >= limit then report.scan_truncated = true; return end
            local props = get(clip, 'GetClipProperty') or {}
            report.media[#report.media + 1] = {
                id = get(clip, 'GetUniqueId'), name = get(clip, 'GetName'), bin = path,
                file_path = props['File Path'], type = props['Type'], fps = props['FPS'],
                resolution = props['Resolution'], duration = props['Duration'],
                start_timecode = props['Start TC'], end_timecode = props['End TC'],
                audio_channels = props['Audio Ch'], sample_rate = props['Sample Rate']
            }
        end
        for _, child in ipairs(get(folder, 'GetSubFolderList') or {}) do
            folder_scan(child, path, depth + 1)
            if report.scan_truncated then return end
        end
    end
    folder_scan(get(get(project, 'GetMediaPool'), 'GetRootFolder'), '', 0)
    report.media_count = #report.media

    local timeline = get(project, 'GetCurrentTimeline')
    report.has_active_timeline = timeline ~= nil
    for index = 1, report.project.timeline_count or 0 do
        local item = get(project, 'GetTimelineByIndex', index)
        report.timelines[#report.timelines + 1] = {
            index = index, name = get(item, 'GetName'), id = get(item, 'GetUniqueId'),
            fps = get(item, 'GetSetting', 'timelineFrameRate')
        }
    end
    if timeline then
        local current = {
            name = get(timeline, 'GetName'), id = get(timeline, 'GetUniqueId'),
            fps = get(timeline, 'GetSetting', 'timelineFrameRate'),
            start_frame = get(timeline, 'GetStartFrame'), end_frame = get(timeline, 'GetEndFrame'),
            start_timecode = get(timeline, 'GetStartTimecode'),
            playhead_timecode = get(timeline, 'GetCurrentTimecode'), tracks = array()
        }
        report.current_timeline = current
        local item_count = 0
        for _, track_type in ipairs({'video', 'audio', 'subtitle'}) do
            for index = 1, get(timeline, 'GetTrackCount', track_type) or 0 do
                local track = {type = track_type, index = index,
                    name = get(timeline, 'GetTrackName', track_type, index),
                    enabled = get(timeline, 'GetIsTrackEnabled', track_type, index),
                    locked = get(timeline, 'GetIsTrackLocked', track_type, index), items = array()}
                current.tracks[#current.tracks + 1] = track
                for _, item in ipairs(get(timeline, 'GetItemListInTrack', track_type, index) or {}) do
                    if item_count >= limit then report.scan_truncated = true; break end
                    local media = get(item, 'GetMediaPoolItem')
                    track.items[#track.items + 1] = {
                        name = get(item, 'GetName'), id = get(item, 'GetUniqueId'),
                        media_id = get(media, 'GetUniqueId'),
                        start_frame = get(item, 'GetStart', true), end_frame = get(item, 'GetEnd', true),
                        duration_frames = get(item, 'GetDuration', true),
                        left_handle_frames = get(item, 'GetLeftOffset', true),
                        right_handle_frames = get(item, 'GetRightOffset', true)
                    }
                    item_count = item_count + 1
                end
            end
        end
        report.timeline_item_count = item_count
    end
    report.render_formats = get(project, 'GetRenderFormats')
    report.mp4_codecs = get(project, 'GetRenderCodecs', 'mp4')
    report.capabilities = {
        project_inspection = 'live_readback',
        media_inspection = 'readback_attempted_see_errors_and_scan_truncated',
        timeline_inspection = timeline and 'readback_attempted_see_errors' or 'no_active_timeline',
        project_export_and_save = 'documented_in_19_sdk_not_tested',
        timeline_duplicate_and_edit = 'documented_in_19_sdk_not_tested',
        fairlight_effect_controls = 'native_ui_required_not_tested',
        audio_transition_controls = 'native_ui_required_not_tested',
        word_timing = 'not_tested_no_provider_configured_by_this_audit',
        waveform_inspection = 'native_ui_or_local_analysis_not_tested',
        preview_render = 'formats_queried_no_render_started',
        listening_and_watchthrough = 'not_performed'
    }
    report.finished_at_utc = os.date('!%Y-%m-%dT%H:%M:%SZ')
    report.status = (#errors > 0 or report.scan_truncated) and 'partial' or 'complete_read_only_snapshot'
    local encoded = json(report)
    if options.output_path then
        local existing = io.open(options.output_path, 'rb')
        if existing then existing:close(); error('Report exists; choose a new output path.') end
        local output, why = io.open(options.output_path, 'wb')
        assert(output, why)
        assert(output:write(encoded .. '\n'))
        assert(output:close())
        print('CODEX_AUDIT_SAVED ' .. options.output_path)
    else
        print('CODEX_AUDIT_JSON ' .. encoded)
    end
    print('CODEX_AUDIT ' .. report.status .. ' | ' .. tostring(report.resolve_version) ..
        ' | ' .. project_name .. ' | media=' .. report.media_count ..
        ' | timelines=' .. tostring(report.project.timeline_count) ..
        ' | active_fps=' .. tostring(report.current_timeline and report.current_timeline.fps) ..
        ' | project_fps=' .. tostring(report.project.frame_rate_setting))
    return report
end
