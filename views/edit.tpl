% rebase('base.tpl', title=title, itson=itson)
<div class="row">&nbsp;</div>
<div class="back">
  <form class="form" action="/admin/sessions/{{ record.id }}" method="POST">
      <h2>{{ title }}</h2>
        <div class="form-group">
          <label>Size</label>
          <input type="text" name="size"
                 placeholder="size..."
                 class="form-control"
                 value="{{ record.size }}"
                  />
        </div>
        <div class="form-group">
          <label>Spot</label>
          <input type="text" name="spot"
                 placeholder="Spot..."
                 class="form-control"
                 value="{{ record.spot }}"
                  />
        </div>
        <div class="form-group">
          <label>Comment</label>
          <input name="comment" placeholder="Comment..."
                 class="form-control"
                 value="{{ record.comment }}" />
        </div>
        <div class="form-group">
          <div class="row">&nbsp;</div>
          <input type="submit" class="btn btn-lg btn-primary"
                 value="Save" />
          <a href="/admin/sessions" class="btn btn-lg btn-danger">Cancel</a>
        </div>
  </form>
</div>
