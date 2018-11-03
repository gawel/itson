% rebase('base.tpl', title=title, itson=itson)
<div class="row">&nbsp;</div>
<div class="back">
<form action="/admin/sessions/new" method="POST">
    <h2>{{ title }}</h2>
    <div class="text-center">
% if itson:
        <input name="comment" placeholder="Comment..."
               class="form-control" />
        <div class="row">&nbsp;</div>
        % for value, label in sizes:
        <div class="form-check form-check-inline btn btn-lg">
            <input type="radio"
                   name="size"
                   id="size_{{value}}"
                   value="{{ value }}"
                   class="form-check-input"
                   %if value == 1:
                   checked="checked"
                   % end
            />
            <label class="form-check-label" for="size_{{ value }}">
                {{ label }}
            </label>
        </div>
        % end
        <div class="row">&nbsp;</div>
        <input type="submit" class="btn btn-lg btn-primary"
               name="stop" value="Stop" />
        <a href="/" class="btn btn-lg btn-danger">Cancel</a>
% else:
        <input type="text" name="new_spot"
               value=""
               placeholder="Spot..."
               class="form-control"
                />
        <div class="row">&nbsp;</div>
        <select name="spot" class="form-control">
            % for spot in spots:
            <option>{{ spot }}</option>
            % end
        </select>
        <div class="row">&nbsp;</div>
        <input type="submit" class="btn btn-lg btn-primary"
               name="start" value="Start" />
        <a href="/" class="btn btn-lg btn-danger">Cancel</a>
% end
    </div>
</form>
</div>
