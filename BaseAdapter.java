package com.okfunc.testvlayout;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.LayoutRes;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.alibaba.android.vlayout.DelegateAdapter;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

public abstract class BaseAdapter<T> extends DelegateAdapter.Adapter<BaseAdapter<T>.BaseAdapterHolder> {

    public interface OnItemClickListener<T> {
        void onItemClick(View clickView, T item, int position, int itemViewType, BaseAdapter<T> adapter, BaseAdapter<T>.BaseAdapterHolder holder);
    }

    public interface Filter<T> {
        boolean filter(Object obj, T item);
    }

    protected Context mContext;
    protected LayoutInflater mLayoutInflater;
    private OnItemClickListener<T> mItemClickListener;
    private final List<T> mData = new ArrayList<>();
    private final List<T> mBackUp = new ArrayList<>();

    public BaseAdapter(@NonNull Context context) {
        mContext = context;
        mLayoutInflater = LayoutInflater.from(mContext);
    }

    public BaseAdapter<T> setOnItemClickListener(OnItemClickListener<T> listener) {
        mItemClickListener = listener;
        return this;
    }

    public BaseAdapter<T> setData(List<T> list) {
        mData.clear();
        if (list != null) mData.addAll(list);
        notifyDataSetChanged();
        return this;
    }

    public BaseAdapter<T> addData(List<T> list) {
        if (list != null) mData.addAll(list);
        notifyDataSetChanged();
        return this;
    }

    public BaseAdapter<T> sort(@NonNull Comparator<T> comparator) {
        if (!mBackUp.isEmpty()) {
            mData.clear();
            mData.addAll(mBackUp);
        }
        mBackUp.clear();
        mBackUp.addAll(mData);
        Collections.sort(mData, comparator);
        notifyDataSetChanged();
        return this;
    }

    public BaseAdapter<T> fillter(Object target, @NonNull Filter<T> filter) {
        if (!mBackUp.isEmpty()) {
            mData.clear();
            mData.addAll(mBackUp);
        }
        mBackUp.clear();
        mBackUp.addAll(mData);
        mData.clear();

        for (T t : mBackUp) {
            if (filter.filter(target, t)) {
                mData.add(t);
            }
        }
        notifyDataSetChanged();
        return this;
    }


    public void restore() {
        if (!mBackUp.isEmpty()) {
            mData.clear();
            mData.addAll(mBackUp);
        }
        mBackUp.clear();
        notifyDataSetChanged();
    }

    public T getItem(int position) {
        return mData.get(position);
    }

    @Override
    public int getItemCount() {
        return mData.size();
    }

    @Override
    protected void onBindViewHolderWithOffset(BaseAdapterHolder holder, int position, int offsetTotal, List<Object> payloads) {
        holder.bindPosition(position, offsetTotal);
        super.onBindViewHolderWithOffset(holder, position, offsetTotal, payloads);
    }

    protected BaseAdapter<T>.BaseAdapterHolder createGenericViewHolder(ViewGroup parent, @LayoutRes int layoutId) {
        return new BaseAdapterHolder(mLayoutInflater.inflate(layoutId, parent, false));
    }

    protected View[] getItemClickViews(BaseAdapterHolder holder, int viewType) {
        return new View[]{holder.itemView};
    }

    public class BaseAdapterHolder extends RecyclerView.ViewHolder implements View.OnClickListener {

        private int position;
        private int offsetTotal;

        public BaseAdapterHolder(@NonNull View itemView) {
            super(itemView);
            setTargetViewClickListener();
        }

        private void bindPosition(int position, int offsetTotal) {
            this.position = position;
            this.offsetTotal = offsetTotal;
        }

        protected void setTargetViewClickListener() {
            View[] views = getItemClickViews(this, getItemViewType());
            if (views != null) {
                for (View view : views) {
                    view.setOnClickListener(this);
                }
            }
        }

        @Override
        public void onClick(View v) {
            OnItemClickListener<T> listener = mItemClickListener;
            if (listener != null) {
                listener.onItemClick(v, getItem(position), position, getItemViewType(), BaseAdapter.this, this);
            }
        }
    }
}
