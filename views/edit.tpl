% rebase('base.tpl', title=title, itson=itson)
<div class="row">&nbsp;</div>
<div class="back">
  <form class="form" action="/admin/sessions/{{ record.id }}" method="POST">
    <h2>{{ title }} session {{ record.id }}</h2>
    % for field in ('date', 'started', 'ended', 'size', 'spot', 'comment'):
      <div class="form-group">
        <label>{{ field.title() }}</label>
        <input type="text" name="{{ field }}"
               placeholder="{{ field.title() }}..."
               class="form-control"
               value="{{ record.get(field) or '' }}"
                />
      </div>
    % end
    <div class="form-group">
      <div class="row">&nbsp;</div>
      <input type="submit" class="btn btn-lg btn-primary"
             value="Save" />
      <a href="/admin/sessions" class="btn btn-lg btn-danger">Cancel</a>
    </div>
  </form>
</div>
